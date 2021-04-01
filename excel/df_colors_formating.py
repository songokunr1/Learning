# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('pandas_conditional.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book
worksheet = writer.sheets['Sheet1']


# Add a format. Light red fill with dark red text.
format1 = workbook.add_format({'bg_color': '#FFC7CE',
                               'font_color': '#9C0006'})

# Set the conditional format range.
start_row = 1
start_col = 3
end_row = len(df)
end_cold = start_col

# Apply a conditional format to the cell range.
worksheet.conditional_format(start_row, start_col, end_row, end_cold,
                             {'type':     'cell',
                              'criteria': '>',
                              'value':    20,
                              'format':   format1})

# Close the Pandas Excel writer and output the Excel file.
writer.save()