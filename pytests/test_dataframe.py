import pandas as pd
import pytest


@pytest.fixture(scope='module')
def df():
    print('--------setup--------')
    df_base = pd.read_csv(
        r"C:\workbench\Ladowanie\2020_12_05\opp_oif_offer\ParentOpportunity\sCRM_ParentOpportunity_2020_08_14_230911.csv")
    index_to_set = 'Id'
    df_base.set_index(index_to_set, inplace=True)
    return df_base


# @pytest.fixture(scope='module')
# def refdata():
#     return pd.DataFrame(
#         data=[
#             ['x', 50],
#             ['y', 30],
#             ['z', 20],
#         ],
#         columns=['A', 'C'],
#     )


# def test_total(mydata, refdata):
#     total = mydata['C'].sum()
#     requirement = refdata['C'].sum()
#     dt.validate(total, requirement)

# def test_single_value(df):
#     value = df.at["index_value", "column_name"]
#     expected = ''
#     assert value == expected


def test_single_value(df):
    value = df.at["0063h000009d477AAA", "Opportunity Number (Formatted)"]
    expected = '19.TR.878184.R.005'
    assert value == expected
