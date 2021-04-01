import pandas as pd
import os
import argparse
import shutil
import GOPSFunctions
import GlobalView
import numpy as np

from math import floor
from datetime import timedelta
from datetime import datetime as dt


class SanityCheck:
    SCHEMA = 'MatlabInput_Processing'
    MASTER_VALUES = {'sales_item': 'sales_item_impacted',
                     'component': 'component_soh',
                     'period': 'primary_demand',
                     'customer': 'primary_demand',
                     'customer_team': 'primary_demand'
                     }

    def __init__(self, table, key):
        self._key = key
        self._table = table

        return

    def validate(self):
        # Built query to download data from database
        query = 'select {} from {}'.format(','.join(self._key), '.'.join([self.SCHEMA, self._table]))
        df = pd.read_sql(sql=query, con=connection())
        key = True  # assume that everything is fine as beggining

        # Key checking - check if no duplicates exist in database
        if df.shape[0] != df.drop_duplicates().shape[0]:
            print('Found duplicated values within key')
            key = False
        else:
            print('Key ok.')

        # Unique values checking - has to be consistent between each table
        for k in self._key:

            # 0 - Hard Commits, 1 - Soft Commits
            for commitment_type in [0, 1]:
                # create test query
                q = 'select distinct {} from {}.'.format(k, self.SCHEMA)  # init query template
                q += '{table_name} where commitment_type in (commitment_type, 2);'  # add placeholder for table name

                master_set = pd.read_sql(
                    sql=q.format(table_name=self.MASTER_VALUES[k], commitment_type=commitment_type),
                    con=connection())
                result_set = pd.read_sql(sql=q.format(table_name=self._table, commitment_type=commitment_type),
                                         con=connection())

                diff = pd.merge(left=master_set, right=result_set, how='outer', indicator=True, on=[k])
                dims = True

                if diff.query("_merge != 'both'").shape[0] > 0:
                    print(k + ' - discrepancies found:')
                    print(diff)
                    dims = False
                else:
                    print(k + ' - no discrepancies found.')

        return {'key': key, 'dims': dims}

    # Obsolete
    # @staticmethod
    # def component_cost():
    #     data = pd.read_sql('select component, comp_cost from {}.component_soh where comp_cost <= 0'.format(SanityCheck.SCHEMA),
    #                        connection())
    #     log('component_soh_comp_cost', data.shape[0] == 0, 1)
    #     return

    # @staticmethod
    # def duplicated_si_names():
    #     print('Checking for sales items with duplicated names')

    #     query = "select distinct sales_item from dbo.sales_item_impacted_h"
    #     sales_items_impacted = pd.read_sql(query, connection())

    #     query = "select distinct aux_linked_si as sales_item, part_description from e2pr.sbom"
    #     sales_items = pd.read_sql(query, connection())
    #     sales_items = sales_items.loc[sales_items['sales_item'].isin(sales_items_impacted['sales_item']), ]

    #     data = sales_items.groupby(by=['sales_item']).size()
    #     data = data.loc[data > 1]

    #     if len(data.loc[data > 1]) != 0:
    #         print('Found duplicated names for following sales items:')
    #         print(sales_items.loc[sales_items['sales_item'].isin(data.index)])
    #     else:
    #         print('No duplicated names found')

    #     return

    @staticmethod
    def prepare(path):
        """
        Creates temporary folder for raw data extraction for SanityCheck script
        :param path:
        :return: Touple- latest file in root, path for extraction, reporting period
        """
        path = os.path.join(path, 'Archive')
        extract_path = os.path.join(path, 'tmp_SanityChecks')

        if os.path.exists(extract_path):
            shutil.rmtree(extract_path)

        # Find latest file in archive root folder
        latest_file = GOPSFunctions.get_latest_file(path)
        os.mkdir(extract_path)

        # Getting file creation date
        filename = os.path.basename(latest_file)
        filename = ''.join(reversed(filename))[4:23]
        filename = ''.join(reversed(filename))[:10]

        creation_date = filename.replace('_', '-')
        reporting_period = GOPSFunctions.Connection.get_reporting_period(creation_date)

        return latest_file, extract_path, reporting_period


def validate_component_coefficient(root):
    print('Validating component coefficient data...')
    table_name = 'component_coefficient'
    table_full_name = '.'.join([SanityCheck.SCHEMA, table_name])

    sbom_file = os.path.join(root, 'sbom.txt')
    sbom = pd.read_table(sbom_file, encoding='ANSI', sep='\t', low_memory=False)
    sbom = sbom.loc[(sbom['aux_linked_si'] == sbom['part']) |
                    (sbom['aux_linked_si'] == sbom['part'].apply(lambda x: x[:x.find('.')]))]

    sbom = sbom[['aux_linked_si', 'component']]
    sbom.columns = ['sales_item', 'part']
    sbom.drop_duplicates(inplace=True)

    bom_file = os.path.join(root, 'bom.txt')
    bom_raw = pd.read_table(bom_file, encoding='ANSI', sep='\t')
    bom_raw['component'] = bom_raw['component'].str.upper()

    bom = pd.merge(left=sbom,
                   right=bom_raw,
                   on=['part'])
    comp_coeff = bom.groupby(by=['sales_item', 'component'])['coefficient'].max().reset_index()

    output = pd.read_sql("select * from " + table_full_name, connection())

    result = pd.merge(left=comp_coeff,
                      right=output,
                      how='inner',
                      indicator=True,
                      on=['sales_item', 'component'])
    result['diff'] = result['coefficient'] - result['comp_coefficient']
    result['diff'] = result['diff'].apply(lambda x: round(x, 3))

    check_values = result.loc[result['diff'] != 0,]

    sc = SanityCheck(table=table_name, key=['sales_item', 'component'])
    check_dims = sc.validate()

    log(table_name,
        check_values.query("diff != 0").shape[0] == 0 and check_values.query("_merge != 'both'").shape[0] == 0,
        check_dims['dims'])

    if check_values.shape[0] > 0:
        print('Error occurred, check log table')
        print(check_values)
    else:
        print('No discrepancies found.')


def validate_sales_item_impacted(root):
    print('Validating sales item data...')
    table_name = 'sales_item_impacted'
    table_full_name = '.'.join([SanityCheck.SCHEMA, table_name])

    soh_file = os.path.join(root, 'si_soh.txt')
    soh_raw = pd.read_table(soh_file, encoding='ANSI', sep='\t')

    plant_file = os.path.join(root, 'plant.txt')
    plant_raw = pd.read_table(plant_file, encoding='ANSI', sep='\t')

    soh = soh_raw.loc[soh_raw.apply(lambda x: str(x['part']).startswith(str(x['aux_linked_si'])), axis=1),]
    soh = pd.merge(left=soh[['aux_linked_si', 'date', 'inv', 'depot', 'depot_orig']]
                   , right=plant_raw[['depot', 'aux_depot_type']]
                   , on=['depot'])
    soh = soh.loc[(soh['aux_depot_type'].str.upper() == 'OHUB')
                  & (soh['depot'] == soh['depot_orig'])]
    soh = soh[['aux_linked_si', 'date', 'inv']].groupby(['aux_linked_si', 'date'])['inv'].sum().reset_index()

    soh['date'] = pd.to_datetime(soh['date'], format='%d/%m/%Y')
    soh.rename(columns={'aux_linked_si': 'sales_item'}, inplace=True)
    # soh['rn'] = soh.sort_values(by=['sales_item', 'date']).groupby(['sales_item']).cumcount() + 1

    output = pd.read_sql('select * from ' + table_full_name, connection())
    dt = GOPSFunctions.add_reporting_period(reporting_period, 5)  # get optimisation starting date

    # take data from week + 5 + 1 due to null and + 1 due to current week
    # result = pd.merge(left=soh.loc[soh['rn'] == 7, ],
    result = pd.merge(left=soh.loc[soh['date'] == pd.to_datetime(dt),],
                      right=output,
                      how='inner',
                      indicator=True,
                      on=['sales_item'])
    result['diff'] = result['inv'] - result['stock_on_hand']
    result['diff'] = result['diff'].apply(lambda x: round(x, 3))

    check_values = result.loc[result['diff'] != 0,]

    sc = SanityCheck(table=table_name, key=['sales_item'])
    check_dims = sc.validate()

    log(table_name,
        check_values.query("diff != 0").shape[0] == 0 and check_values.query("_merge !=  'both'").shape[0] == 0,
        check_dims['dims'])

    if check_values.shape[0] > 0:
        print('Error occurred, check log table')
        print(check_values)
    else:
        print('No discrepancies found.')


def validate_primary_demand(root):
    print('Validating primary demand data.')
    table_name = 'primary_demand'
    table_full_name = '.'.join([SanityCheck.SCHEMA, table_name])

    prim_dem_file = os.path.join(root, 'primary_demand.txt')
    prim_dem_raw = pd.read_table(prim_dem_file, encoding='ANSI', sep='\t', low_memory=False)

    prim_dem = prim_dem_raw.groupby(by=['aux_linked_si'])['req_qty'].sum().reset_index()
    prim_dem.rename(columns={'aux_linked_si': 'sales_item'}, inplace=True)

    output = pd.read_sql('select * from ' + table_full_name,
                         con=connection())
    output = output.groupby(by=['sales_item'])['demand'].sum().reset_index()

    result = pd.merge(left=prim_dem,
                      right=output,
                      how='inner',
                      indicator=True,
                      on=['sales_item'])
    result['diff'] = result['req_qty'] - result['demand']
    result['diff'] = result['diff'].apply(lambda x: round(x, 3))

    check_values = result.loc[result['diff'] != 0,]
    log(table_name,
        check_values.query("diff != 0").shape[0] == 0 and check_values.query("_merge != 'both'").shape[0] == 0,
        1)

    if check_values.shape[0] > 0:
        print('Error occurred, check log table')
    else:
        print('No discrepancies found.')

    return


def validate_capacity(root):
    print('Validating capacity calculations.')
    table_name = 'capacity'
    table_full_name = '.'.join([SanityCheck.SCHEMA, table_name])

    capacity_bill_file = os.path.join(root, 'capacity_bill.txt')
    capacity_bill = pd.read_table(capacity_bill_file, encoding='ANSI', sep='\t')

    capacity_bill = capacity_bill[['part', 'capacity', 'coefficient']]
    capacity_bill['part'] = capacity_bill['part'].apply(lambda x: x[:(x.find('.') if x.find('.') > 0 else len(x))])
    capacity_bill.rename(columns={'part': 'sales_item'}, inplace=True)

    capacity_bill = capacity_bill.groupby(by=['sales_item', 'capacity'])['coefficient'].max().reset_index()

    capacity_utilization_file = os.path.join(root, 'capacity_utilization.txt')
    capacity_utilization = pd.read_table(capacity_utilization_file, encoding='ANSI', sep='\t')

    capacity_utilization = capacity_utilization[['capacity', 'effective_date', 'avl_qty']]
    capacity_utilization['effective_date'] = pd.to_datetime(capacity_utilization['effective_date'],
                                                            format='%d/%m/%Y')
    capacity = pd.merge(left=capacity_bill,
                        right=capacity_utilization,
                        on=['capacity'],
                        how='inner')

    # Downloads primary demand data from Matlabinput
    primary_demand = pd.read_sql("select * from {}.primary_demand".format(SanityCheck.SCHEMA), con=connection())
    calendar = pd.read_sql(
        "select ReportingPeriod, min(FullDate) as effective_date from auxiliary.calendar group by ReportingPeriod"
        , con=connection())

    # Get date based on period
    primary_demand = pd.merge(left=primary_demand
                              , right=calendar
                              , left_on=['period']
                              , right_on=['ReportingPeriod']).drop(columns=['ReportingPeriod'], axis=1)

    # Aggregate to SI level
    si_demand = primary_demand.groupby(by=['sales_item', 'effective_date'], as_index=False)['demand'].sum()
    si_demand['effective_date'] = pd.to_datetime(si_demand['effective_date'])

    # Remove from capacity not impacted SIs
    impacted = pd.read_sql('select * from ' + table_full_name, connection())
    capacity = capacity.loc[capacity['sales_item'].isin(impacted['sales_item']),]

    group_demand = pd.merge(left=capacity[['sales_item', 'effective_date', 'capacity']].drop_duplicates(),
                            right=si_demand,
                            on=['sales_item', 'effective_date']
                            ).groupby(by=['capacity', 'effective_date'], as_index=False)['demand'].sum()

    group_capacity = capacity_utilization.groupby(by=['capacity', 'effective_date'], as_index=False)['avl_qty'].sum()
    si_capacity = pd.merge(left=capacity[['sales_item', 'capacity', 'effective_date', 'coefficient']],
                           right=group_capacity,
                           on=['capacity', 'effective_date'])

    coeff = pd.merge(left=si_capacity, right=si_demand, how='left', on=['sales_item', 'effective_date'])
    coeff = pd.merge(left=coeff, right=group_demand, how='left', on=['capacity', 'effective_date'])

    coeff.rename(columns={'demand_x': 'sales_item_demand',
                          'demand_y': 'group_demand'},
                 inplace=True)
    coeff['coeff'] = coeff.apply(
        lambda x: 0 if x['group_demand'] == 0 else x['sales_item_demand'] / x['group_demand'] / x['coefficient']
        , axis=1)
    coeff['total_capacity'] = coeff.apply(
        lambda x: floor(round(x['coeff'] * x['avl_qty'], 3)) if x['coeff'] == x['coeff'] else 0
        , axis=1)

    output = pd.read_sql('select * from ' + table_full_name, connection())
    output.loc[output['capacity'] == 999999, 'capacity'] = 0

    result = output.groupby(by=['sales_item'])['capacity'].sum().reset_index()

    values_check = pd.merge(left=result,
                            right=coeff.groupby(by=['sales_item'])['total_capacity'].sum().reset_index(),
                            how='outer',
                            indicator=True,
                            on=['sales_item'])
    values_check.rename(columns={'total_capacity': 'raw_capacity', 'capacity': 'db_capacity'}, inplace=True)

    values_check.loc[values_check['raw_capacity'] != values_check['raw_capacity'], 'raw_capacity'] = 0

    values_check['diff'] = values_check['db_capacity'] - values_check['raw_capacity']
    values_check['diff'] = values_check['diff'].apply(lambda x: round(x, 3))

    sc = SanityCheck(table='capacity', key=['sales_item', 'period'])
    dims_check = sc.validate()

    log(table_name,
        values_check.query("diff != 0").shape[0] == 0 and values_check.query("_merge != 'both' and diff != 0").shape[
            0] == 0,
        dims_check['dims'])

    if values_check.query("diff != 0").shape[0] > 0:
        print('Error occurred, check log table')
        print(values_check.query("diff != 0"))
    else:
        print('No discrepancies found.')

    return


def validate_component_data(root, extract_path):
    print('Validating component data.')
    soh_table = 'component_soh'
    supply_table = 'component_supply'

    # Process only HC data
    soh_output = pd.read_sql(
        'select * from {}.{} where commitment_type in (0, 2)'.format(SanityCheck.SCHEMA, soh_table), connection())
    supply_output = pd.read_sql(
        'select * from {}.{} where commitment_type in (0, 2)'.format(SanityCheck.SCHEMA, supply_table), connection())

    # Obsolete - moved into separate function
    # query = "select dateadd(week, 2, min(FullDate)) as date from Auxiliary.calendar where ReportingPeriod = {}"
    # query = query.format(reporting_period)
    # dt = connection().execute(query).fetchone()['date']
    # ########

    dt = GOPSFunctions.add_reporting_period(reporting_period, 2)

    parsed_components = []
    soh_discrepancy = []
    supply_discrepancy = []

    gv = GlobalView.GlobalViewFolder(root, connection())
    gv.extract(extract_path)
    gv.sort()

    for file in gv.files:
        _file = GlobalView.ComponentFile(file.path)

        try:
            _file.parse()
        except GlobalView.CellValueError:
            continue
        except GlobalView.InputError:
            continue

        _component = _file.component

        if _component in parsed_components:
            continue

        _data = _file.to_dict()

        if len(_data['material_balance']) > 0:
            _data_soh = pd.DataFrame(_data['material_balance'])
            _data_soh = _data_soh.loc[_data_soh['depot'].str.startswith('TOTAL'),]

            _data_soh['date'] = pd.to_datetime(_data_soh['date'], format='%Y/%m/%d')
            _data_soh = _data_soh.loc[_data_soh['date'] == dt]

            _soh_raw = _data_soh['material_balance']

            # Check if there are multiple depots available
            if _soh_raw.shape[0] > 1:  # if there is more then one try to take only TOTAL
                _soh_raw = _data_soh.loc[_data_soh['depot'] == 'TOTAL']['material_balance']

                if _soh_raw.shape[
                    0] == 0:  # if there is no 'TOTAL' depot consider only one with the lowest stock on hand
                    _soh_raw['rn'] = _data_soh.groupby(by=['depot']).sort_values(by=['material_balance']).cumcount() + 1
                    _soh_raw = _soh_raw.loc[_soh_raw['rn'] == 1]['material_balance']

            elif _soh_raw.shape[0] == 1:  # if there is only one depot take data from that depot
                _soh_raw = _data_soh['material_balance']
        else:
            _soh_raw = 0

        # Take stock on hand value from the MatlabInput
        _soh_output = soh_output.loc[soh_output['component'] == str(_component)]['stock_on_hand']

        if _soh_output.shape[0] == 0:
            continue

        elif _soh_output.shape[0] > 1:
            GOPSFunctions.raise_error("Found duplicated entry for component {0}:".format(_component))
            continue

        elif round(_soh_raw.sum() - _soh_output.sum(), 3) != 0:
            soh_discrepancy.append({'component': _component, 'raw_data': _soh_raw.sum(), 'output': _soh_output.sum()})

        if len(_data['supply']) > 0:
            _data_supply = pd.DataFrame(_data['supply'])

            _data_supply = _data_supply.loc[_data_supply['depot'].str.startswith('TOTAL'),]
            _data_supply = _data_supply.groupby(by=['component', 'depot', 'date'], as_index=False)['supply'].sum()

            _data_supply['supply_cumulative'] = _data_supply.sort_values(by=['date'])['supply'].cumsum()
            _data_supply.loc[_data_supply['supply_cumulative'] < 0, 'supply'] = 0

            _supply_raw = _data_supply['supply'].sum()
        else:
            _supply_raw = 0

        # Take supply value from the MatlabInput
        _supply_output = supply_output.query("component == '{0}'".format(_file.component))['comp_supply'].sum()

        if round(_supply_raw - _supply_output) != 0:
            supply_discrepancy.append({'component': _component, 'raw_data': _supply_raw, 'output': _supply_output})
            continue

        parsed_components.append(_component)

    if len(soh_discrepancy) > 0:
        GOPSFunctions.raise_error('Found discrepancies in Stock on hand data for following components:')
        print(pd.DataFrame(soh_discrepancy))
    else:
        print('No discrepancies found for stock on hand data.')

    if len(supply_discrepancy) > 0:
        GOPSFunctions.raise_error('Found discrepancies in supply data for following components:')
        print(pd.DataFrame(supply_discrepancy))
    else:
        print('No discrepancies found in supply data.')

    log(soh_table, len(soh_discrepancy) == 0, len(soh_discrepancy) == 0)
    log(supply_table, len(supply_discrepancy) == 0, len(supply_discrepancy) == 0)

    return


def validate_financial_data():
    # download most recent pricing data
    pricing_data = pd.read_sql("select * from Prod1M.NPTAnalyticsPricingData"
                               " where 1=1 \
                               and NPTA_SI_CLP > 0 \
                               and NPTA_CUSI_QTY > 0 \
                               and NPTA_CUSI_CLP > 0 \
                               and isnull(NPTR_SI_Code, '-1') like '47%' \
                               and isnull(iif(NPTA_SI_MRP = 0, NPTA_SI_IRP, NPTA_SI_MRP), 0) > 0 \
                               and NPTA_SI_CLP < NPTA_SI_MRP \
                               and NPTA_SI_CNP < NPTA_SI_CLP \
                               and NPTA_SI_CNP < NPTA_SI_MRP",
                               con=connection())

    columns = {'NPTA_H_RecId': 'rec_id',
               'NPTR_H_OpportunityId': 'opportunity_id',
               'CMDAccountId': 'customer',
               'CMDCTName': 'customer_team',
               'CMDMarketId': 'market',
               'NPTR_SI_Code': 'sales_item',
               'NPTR_SH_PortfolioPackage': 'portfolio_package',
               'NPTR_SH_BusinessLine': 'business_line',
               'NPTR_SI_CategoryName': 'si_category',
               'NPTA_SI_MRP': 'si_mrp',
               'NPTA_SI_IRP': 'si_irp',
               'NPTA_SI_CLP': 'si_clp',
               'NPTA_SI_CNP': 'si_cnp',
               'NPTA_CUSI_QTY': 'cusi_qty',
               'NPTA_CUSI_CLP': 'cusi_clp',
               'NPTA_CUSI_CNP': 'cusi_cnp',
               'NPTR_PHD_DeliveryYear': 'delivery_year',
               'NPTR_PH_SelectedForLoA': 'loa',
               'NPTR_CU_Optional': 'optional'}

    pricing_data = pricing_data[list(columns.keys())]  # select only relevant columns
    pricing_data.rename(columns=columns, inplace=True)  # rename and standardise column names

    pricing_data['curr_year_delivery'] = pricing_data['delivery_year'].apply(lambda x: 0 if x != 2019 else 1)
    pricing_data['loa_selection'] = pricing_data.apply(lambda x: x['loa'] * (1 - x['optional']), axis=1)
    pricing_data['si_mrp'] = pricing_data.apply(lambda x: x['si_irp'] if x['si_mrp'] == 0 else x['si_mrp'], axis=1)

    clp_priorities = ['customer_team', 'market']  # priorities how avg price should be assigned

    # download si-ct pairs that need financial data assignment
    scope = pd.read_sql(
        "select distinct sales_item, customer_team, market from {}.primary_demand where customer_team <> 'N/A'".format(
            SanityCheck.SCHEMA),
        con=connection())
    # add columns to be filled
    scope['idx'] = scope.index
    scope['price'] = 0.0

    scope['cost'] = 0.0
    scope['profit'] = 0.0

    # first fill cost data
    cost_data = pd.read_sql(
        "select SalesItem_ID as sales_item, PSPC as cost from DataStore.SWDActualCost where Active = 1 and ValidTo is null",
        connection())
    cost_to_update = pd.merge(left=scope[['sales_item', 'idx']],
                              right=cost_data,
                              on=['sales_item'])
    cost_to_update.set_index('idx', inplace=True)
    scope.update(cost_to_update)

    # Sort and aggregate data to prepare for
    ordering = ['loa_selection', 'curr_year_delivery']
    ordering_data = pricing_data[ordering].drop_duplicates()
    ordering_data = ordering_data.sort_values(by=ordering, ascending=[False, False]).values

    # assign prices in a given priorities
    for priority in clp_priorities:
        for od in ordering_data:
            (loa_selection, delivery_year) = od

            # select only relevant data from the pricing data
            _pricing_data = pricing_data.loc[(pricing_data['loa_selection'] == loa_selection)
                                             & (pricing_data['curr_year_delivery'] == delivery_year)]
            _pricing_data = _pricing_data.groupby(by=['sales_item', priority], as_index=False)[
                ['cusi_clp', 'cusi_qty']].sum()
            _pricing_data['price'] = _pricing_data['cusi_clp'] / _pricing_data['cusi_qty']  # price calculation

            # select only those si-ct pairs that requires updating
            _to_update = pd.merge(left=scope.query("price == 0").drop(columns='price'),
                                  right=_pricing_data,
                                  on=['sales_item', priority])
            _to_update.set_index('idx', inplace=True)  # add artificial index to be able to update scope df
            scope.update(_to_update[['price']])

    # download relevant data from database
    discount_data = pd.read_sql("with cte as (\
    select distinct\
        sales_item\
        , customer_team\
        , market\
        from {}.primary_demand) \
    select \
        c.* \
        , d.ENSI_IRP as irp \
        , d.GICM_Lcode as portfolio_package \
        , d.GICM_PCBusinessLine as business_line \
        , case when d.GICM_GeneralSalesItemType = '13-Service' then 'Service' \
            when d.GICM_GeneralSalesItemType = '11-HW' then 'Hardware' \
            when d.GICM_GeneralSalesItemType = '12-SW' then 'Software' \
            end as si_category \
        , convert(decimal(17,4), 0.0) as discount \
    from  cte as c inner join DataStore.EnoviaSalesItems as d on c.sales_item = d.ENSI_SalesItemID;".format(
        SanityCheck.SCHEMA),
                                connection())
    discount_data['idx'] = discount_data.index

    irp_data = pd.read_sql(
        "select NPTR_SI_Code as sales_item, avg(NPTA_SI_IRP) as irp from Prod1M.NPTAnalyticsPricingData group by NPTR_SI_Code",
        connection())
    irp_to_update = pd.merge(left=discount_data.query("irp == 0").drop(columns=['irp']),
                             right=irp_data,
                             on=['sales_item'])

    irp_to_update.set_index('idx', inplace=True)
    discount_data.update(irp_to_update['irp'])

    discount_priorities = ['portfolio_package', 'business_line', 'si_category']

    for discount in discount_priorities:  # loop through discounts
        for clp in clp_priorities:  # loop through clp priorities
            for od in ordering_data:
                (loa_selection, delivery_year) = od

                _discount_data = pricing_data.loc[(pricing_data['loa_selection'] == loa_selection)
                                                  & (pricing_data['curr_year_delivery'] == delivery_year)]
                _discount_data['cusi_mrp'] = _discount_data['si_mrp'] * _discount_data['cusi_qty']

                _discount_data = _discount_data.groupby(by=[clp, discount], as_index=False)[
                    ['cusi_mrp', 'cusi_clp', 'cusi_qty']].sum()

                _discount_data['irp'] = _discount_data['cusi_mrp'] / _discount_data['cusi_qty']
                _discount_data['clp'] = _discount_data['cusi_clp'] / _discount_data['cusi_qty']

                _discount_data['discount'] = _discount_data['clp'] / _discount_data['irp']
                _discount_data['discount'] = _discount_data['discount'].apply(lambda x: round(x, 4))

                _to_update = pd.merge(left=discount_data.query("discount == 0").drop(columns=['discount']),
                                      right=_discount_data,
                                      on=[discount, clp])
                _to_update.set_index('idx', inplace=True)

                discount_data.update(_to_update)

    # At least update 0-values IRP from NPT with raw data from Enovia
    enovia = pd.read_sql("select ENSI_SalesItemID, ENSI_IRP from DataStore.EnoviaSalesItems",
                         connection())
    enovia.columns = ['sales_item', 'irp']

    irp_to_update = pd.merge(left=discount_data.query("irp == 0").drop(columns=['irp']),
                             right=enovia,
                             on=['sales_item'])

    irp_to_update.set_index('idx', inplace=True)
    discount_data.update(irp_to_update['irp'])

    discount_data['price'] = discount_data['irp'] * discount_data['discount']
    price_to_update = pd.merge(left=scope.query("price == 0").drop(columns='price'),
                               right=discount_data[['sales_item', 'customer_team', 'price']],
                               on=['sales_item', 'customer_team'])
    price_to_update.set_index('idx', inplace=True)

    scope.update(price_to_update['price'])
    scope['profit'] = scope['price'] - scope['cost']

    scope = scope.query("price > 0")  # remove SIs that have no price assigned

    values = ['price', 'profit']
    for value in values:
        matrix = pd.read_sql(
            "select * from {}.matrix_{} where customer_team <> 'N/A'".format(SanityCheck.SCHEMA, value),
            connection())
        x = pd.merge(left=scope.groupby(by=['sales_item', 'customer_team'], as_index=False)[value].mean(),
                     right=matrix,
                     on=['sales_item', 'customer_team'])
        x.rename(columns={value + '_x': 'raw', value + '_y': 'db'}, inplace=True)
        x['diff'] = (x['raw'] - x['db']).apply(lambda x: abs(round(x, 2)))

        diffs = x.query("diff > 0")

        sanity_check = SanityCheck(table='matrix_' + value, key=['customer_team', 'sales_item'])
        sanity_check = sanity_check.validate()

        log(table_name='matrix_' + value,
            values=diffs.query("diff == 0").shape[0] == 0,
            dims=sanity_check['dims'])

        if sanity_check['dims']:
            print("Matrix_{} - dims os".format(value))
        else:
            GOPSFunctions.raise_error("Found discrepancies in dims.")

        if diffs.query("diff == 0").shape[0] == 0:
            print("Matrix_{} - values ok".format(value))
        else:
            GOPSFunctions.raise_error("Found discrepancies for matrix_{}".format(value))


def validate_tnc_data():
    scope = pd.read_sql("select distinct customer_team from {}.primary_demand".format(SanityCheck.SCHEMA)
                        , connection())
    scope['ct_redbox'] = scope['customer_team'].str.upper()
    global reporting_period

    redbox_query = "select {} from Prod1M.RedBoxCustomerData where {} group by {}".format(
        ','.join(['upper(RedC_CT) as RedC_CT',
                  'sum(RedC_NetSales) * 0.1 as Penalty',
                  'RedC_MasterCategory'
                  ])
        , ' and '.join(["RedC_BG = 'MN'",
                        "RedC_MeasureEntityType = 'PL'",
                        "RedC_NetSales > 0",
                        "RedC_CustomerGroupType = 'CT'",
                        "RedC_Year >= datepart(year, dateadd(m, -1, (select min(FullDate) from Auxiliary.Calendar where ReportingPeriod = '" + reporting_period + "')))",
                        "RedC_Quarter >= datepart(quarter, dateadd(m, -1, (select min(FullDate) from Auxiliary.Calendar where ReportingPeriod = '" + reporting_period + "')))",
                        "RedC_CT is not null"
                        ])
        , ','.join(['RedC_CT', 'RedC_MasterCategory'])
    )
    redbox = pd.read_sql(redbox_query, connection())
    redbox.columns = ['ct_redbox', 'penalty', 'category']
    redbox.to_csv(r"I:\GIT\Nokia.DataPlatform.Etl.Gops\scripts\redbox.csv")

    filters = ['LE', 'Plan']

    tnc = scope.copy()
    tnc.to_csv(r"I:\GIT\Nokia.DataPlatform.Etl.Gops\scripts\tnc.csv")


    for f in filters:
        tnc = pd.merge(left=tnc, right=redbox.query("category == '{}'".format(f)), how='left', on=['ct_redbox'])
        tnc.to_csv(fr"I:\GIT\Nokia.DataPlatform.Etl.Gops\scripts\marge_{f}.csv")
        tnc.drop(columns={'category'}, inplace=True)
        tnc.rename(columns={'penalty': 'penalty_{}'.format(f.lower())}, inplace=True)

    tnc['penalty'] = tnc.apply(lambda x: x['penalty_le'] if x['penalty_le'] == x['penalty_le'] else x['penalty_plan'],
                               axis=1)
    tnc.loc[tnc['penalty'].isnull(), 'penalty'] = 0
    tnc['penalty'] = tnc['penalty'] * 10 ** 6

    tnc.loc[tnc['ct_redbox'] == 'NAM SP CT SPRINT', 'penalty'] = tnc['penalty'] * 1.5
    tnc.loc[tnc['ct_redbox'] == 'NAM TMO CT T-MOBILE US', 'penalty'] = tnc['penalty'] * 0.5
    tnc.loc[tnc['ct_redbox'] == 'NAM VER CT VERIZON WIRELESS', 'penalty'] = tnc['penalty'] * 0.4

    tnc_sc = tnc[['ct_redbox', 'penalty']].drop_duplicates()
    tnc_sc.rename(columns={'ct_redbox': 'customer_team', 'penalty': 'penalty_sc'}, inplace=True)

    result = pd.read_sql("select * from {}.redbox_customers_risk".format(SanityCheck.SCHEMA), connection())
    result.rename(columns={'Penalty': 'penalty_db'}, inplace=True)

    values_checks = pd.merge(left=tnc_sc, right=result, on=['customer_team'])
    values_checks['diff'] = values_checks['penalty_db'] - values_checks['penalty_sc']
    values_checks['diff'] = values_checks['diff'].apply(lambda x: round(x, 0))
    values_checks.to_csv(r"I:\GIT\Nokia.DataPlatform.Etl.Gops\scripts\values_checks.csv")

    values_checks.query("diff != 0")
    sc = SanityCheck(table='redbox_customers_risk', key=['customer_team'])
    dims_check = sc.validate()

    log(table_name='redbox_customers_risk'
        , values=values_checks.query("diff != 0").shape[0] == 0
        , dims=dims_check['dims'])

    return


# Obsolete
# def validate_historical_list():
#     tables = {'sales_item_impacted_h': ['sales_item_impacted', 'sales_item'],
#               'critical_components_h': ['component_soh', 'component']
#               }
#
#     last_export = connection().execute("select max(planning_week) as pw from component.imports").fetchone()['pw']
#
#     for table, data in tables.items():
#         query = "select {} from dbo.{} where planning_week = '{}'".format(data[1], table, last_export)
#         df = pd.read_sql(sql=query, con=connection())
#
#         query = "select {} from {}.{}".format(data[1], SanityCheck.SCHEMA, data[0])
#         ref_df = pd.read_sql(sql=query, con=connection())
#
#         sc = pd.merge(left=df, right=ref_df, how='outer', on=data[1])
#         if sc.shape[0] != df.shape[0] or sc.shape[0] != ref_df.shape[0]:
#             print('Found discrepancies.')
#             print(sc)
#             log(table_name=table, values=0, dims=0)
#         else:
#             log(table_name=table, values=1, dims=1)
#             print('Ok.')
#
#     return


def connection():
    return GOPSFunctions.Connection.engine()


def log(table_name, values=None, dims=None):
    global reporting_period
    GOPSFunctions.Connection.sanity_check_log(step='Sanity Checks'
                                              , table_name=table_name
                                              , dims=dims
                                              , values=values
                                              , reporting_period=reporting_period)
    return


def validate_soft_commits(path):
    start_week = GOPSFunctions.add_reporting_period(reporting_period)
    start_week = pd.to_datetime(start_week)
    end_week = start_week + timedelta(days=21)

    start_week = pd.to_datetime(start_week)
    end_week = start_week + timedelta(days=21)

    # Soft commits data
    soft_commits_raw = pd.read_csv(os.path.join(path, 'component_soft_commits.txt'), encoding='ANSI', sep='\t')
    component_inv_raw = pd.read_csv(os.path.join(path, 'component_inv.txt'), encoding='ANSI', sep='\t')

    impacted_si = pd.read_sql("select sales_item from {}.sales_item_impacted".format(SanityCheck.SCHEMA),
                              con=connection())

    # Import BoM data
    bom_raw = pd.read_csv(os.path.join(path, 'bom.txt'), encoding='ANSI', sep='\t')
    bom = bom_raw.copy()[['depot', 'part', 'component', 'coefficient']]
    bom['sales_item'] = bom['part'].apply(lambda x: x[: x.find('.')] if x.find('.') > 0 else x)
    bom = bom.loc[bom['sales_item'].isin(impacted_si['sales_item'])]  # keep only impacted SI

    bom_agg = pd.read_sql("select * from {}.component_coefficient".format(SanityCheck.SCHEMA), con=connection())
    bom_agg.rename(columns={'comp_coefficient': 'coefficient'}, inplace=True)
    bom_agg = bom_agg[['sales_item', 'component', 'coefficient']]

    # Version item supply
    vi_supply_raw = pd.read_csv(os.path.join(path, 'vi_supply_plan.txt'), encoding='ANSI', sep='\t')
    vi_supply = vi_supply_raw[['part',
                               'aux_linked_si',
                               'depot_orig',
                               'depot',
                               'aux_depot_type',
                               'date',
                               'exec_wcd']].copy()
    vi_supply.rename(columns={'aux_linked_si': 'sales_item'}, inplace=True)
    vi_supply = vi_supply.loc[vi_supply['depot_orig'] == vi_supply['depot']]  # remove logistic operations
    vi_supply = vi_supply.loc[vi_supply['sales_item'].isin(impacted_si['sales_item'])]

    # Select relevant time period
    vi_supply['date'] = pd.to_datetime(vi_supply['date'], format="%d/%m/%Y")
    vi_supply = vi_supply.loc[vi_supply['date'] >= start_week]
    vi_supply = vi_supply.loc[vi_supply['date'] <= end_week]

    # Agg to total production
    supply = vi_supply.groupby(by=['part', 'sales_item', 'depot'], as_index=False)['exec_wcd'].sum()

    # Find missing BoM's entires
    missing_scope = supply[['part', 'sales_item', 'depot']].drop_duplicates()  # find all relevant si-depot pairs
    missing_scope = pd.merge(left=missing_scope,
                             right=bom[['part', 'sales_item', 'depot', 'component']].drop_duplicates(),
                             how='left',
                             on=['part', 'sales_item', 'depot'])
    missing_scope = missing_scope.loc[missing_scope['component'].isnull()]

    bom_missing = pd.merge(left=missing_scope.drop(columns=['component']),
                           right=bom_agg,
                           how='left',
                           on=['sales_item'])

    # Concat BoMs
    bom_matched = pd.merge(left=bom[['part', 'sales_item', 'depot', 'component', 'coefficient']],
                           right=bom_missing,
                           how='left',
                           on=['part', 'depot', 'component'])
    bom_matched = bom_matched.loc[bom_matched['coefficient_y'].isnull()]
    bom_matched.drop(columns=['sales_item_y', 'coefficient_y'], inplace=True)
    bom_matched.rename(columns={'sales_item_x': 'sales_item', 'coefficient_x': 'coefficient'}, inplace=True)
    bom_matched = pd.merge(left=bom_matched,
                           right=vi_supply[['part', 'depot']].drop_duplicates(),
                           on=['part', 'depot'])

    bom_total = pd.concat([bom_matched, bom_missing])

    component_usage = pd.merge(left=supply,
                               right=bom_total.drop(columns=['sales_item']),
                               on=['part', 'depot'])

    # Get component usage = vi production * component coefficient
    component_usage['comp_demand'] = component_usage['exec_wcd'] * component_usage['coefficient']
    # Calculate component demand
    comp_demand = component_usage.groupby(by=['component'], as_index=False)['comp_demand'].sum()

    # Process soft commits
    soft_commits = soft_commits_raw.copy()
    soft_commits['arrival_date'] = pd.to_datetime(soft_commits_raw['arrival_date'], format="%d/%m/%Y")
    soft_commits = soft_commits.loc[soft_commits['arrival_date'] >= start_week]

    comp_demand = comp_demand.loc[comp_demand['component'].isin(soft_commits['part'])]  # take only relevant components
    comp_supply = soft_commits.loc[soft_commits['arrival_date'] <= end_week]  # to get material balance

    component_supply = comp_supply.groupby('part', as_index=False)['qty'].sum()

    # Component soh @ begginig week
    component_inv = component_inv_raw.copy()
    component_inv = component_inv.loc[component_inv['depot'] == component_inv['depot_orig']]

    component_inv = component_inv.groupby(by=['part'], as_index=False)['qty_free_stock'].sum()

    component_material_balance = \
        pd.merge(left=component_supply,
                 right=component_inv,
                 how='left',
                 on='part')

    component_material_balance = \
        pd.merge(left=component_material_balance,
                 right=comp_demand,
                 how='left',
                 left_on=['part'],
                 right_on=['component']).drop(columns=['component'])

    component_material_balance.columns = ['component', 'supply', 'soh', 'demand']
    component_material_balance.fillna(0, inplace=True)

    component_material_balance['material_balance'] = \
        component_material_balance['supply'] + component_material_balance['soh'] - component_material_balance['demand']

    # Compare data with DB calculations
    # Download soft commits data from DB
    component_material_balance_db = pd.read_sql(
        "select component, stock_on_hand from {}.component_soh where commitment_type in (1, 2);".format(
            SanityCheck.SCHEMA), connection())
    results = pd.merge(left=component_material_balance[['component', 'material_balance']],
                       right=component_material_balance_db,
                       on=['component'])
    results['diff'] = results['stock_on_hand'] - results['material_balance']
    results['diff'] = results['diff'].apply(lambda x: round(x, 3))

    if results.query('diff != 0').shape[0] != 0:
        print('Error occurred, check log table')
        print(results.query("diff != 0"))
    else:
        print("No discrepancies found.")

    log(table_name='soft_commits-material balance'
        , values=results.query("diff != 0").shape[0] == 0
        , dims=1)


def validate_soft_commits_supply(path):
    soft_commits_supply = pd.read_csv(os.path.join(path, 'component_soft_commits.txt'), sep='\t', encoding='ANSI')
    soft_commits_supply = soft_commits_supply.groupby(by=['part'], as_index=False)['qty'].sum()

    soft_commits_supply_db = pd.read_sql(
        "select * from {}.component_supply where commitment_type in (1, 2)".format(SanityCheck.SCHEMA), connection())
    soft_commits_supply_db = soft_commits_supply_db.groupby(by=['component'], as_index=False)['comp_supply'].sum()

    results = pd.merge(left=soft_commits_supply,
                       right=soft_commits_supply_db,
                       left_on=['part'],
                       right_on=['component'])
    results['diff'] = results['qty'] - results['comp_supply']
    results['diff'] = results['diff'].apply(lambda x: round(x, 3))

    if results.query('diff != 0').shape[0] != 0:
        print('Error occurred, check log table')
        print(results.query("diff != 0"))
    else:
        print("No discrepancies found.")

    log(table_name='soft_commits-supply'
        , values=results.query("diff != 0").shape[0] == 0
        , dims=1)


def validate_calcualtions(path):
    validate_component_coefficient(path)
    validate_sales_item_impacted(path)

    # validate_primary_demand(path)
    validate_capacity(path)

    validate_soft_commits(path)
    validate_soft_commits_supply(path)


parser = argparse.ArgumentParser(description='Validates calculations made on SQL server.')
parser.add_argument('-e2pr', action='store', dest='e2pr', help='Path to E2PR export data.')
parser.add_argument('-env', action='store', dest='env', help='Working environment')
parser.add_argument('--gv', action='store', dest='gv', help='Path to global view component.')

args = parser.parse_args()

e2pr_path = args.e2pr  # path to the E2PR azure folder
env = GOPSFunctions.Env(args.env)  # running environment

# Validating calculation data base on E2PR files
(e2pr_latest_file, e2pr_extract_path, reporting_period) = SanityCheck.prepare(e2pr_path)
#
# Remove existing sanity check logs
GOPSFunctions.Connection.sanity_check_truncate('Sanity Checks', reporting_period)
GOPSFunctions.extract_zip(e2pr_latest_file, e2pr_extract_path)  # extract raw files
try:
    validate_calcualtions(e2pr_extract_path)  # run sanity checks
finally:
    shutil.rmtree(e2pr_extract_path)  # remove extracted files

# gv_path = args.gv  # path to the GV (components) folder
# if gv_path:
#    # Validating component data
#    (gv_latest_file, gv_extract_path, reporting_period) = SanityCheck.prepare(gv_path)
#    try:
#        #run test
#        validate_component_data(os.path.dirname(gv_latest_file), gv_extract_path)
#    finally:
#        shutil.rmtree(gv_extract_path)  # remove extracted files
# Run not raw-data related test
validate_financial_data()
validate_tnc_data()
