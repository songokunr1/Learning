df[["End Customer Account Number", "End Customer Account", "Activity Sector", "Market Segment"]]

df[["End Customer Account Number", "End Customer Account", "Activity Sector", "Market Segment"]][df['End Customer Account Number'] == 301033387.0]

df[["End Customer Account Number", "End Customer Account", "Activity Sector", "Market Segment"]][df['End Customer Account Number'] == 301033387.0]
import pandas as pd

lista = df['End Customer Account Number'].tolist()

columns = ["End Customer Account Number", "End Customer Account", "Activity Sector", "Market Segment"]
end=[]
name=[]
sektor=[]
segment=[]
for single in lista:
    try:
        b = df[["End Customer Account Number", "End Customer Account", "Activity Sector", "Market Segment"]][
            df['End Customer Account Number'] == single].iloc[0]
        end.append(b["End Customer Account Number"])
        name.append(b["End Customer Account"])
        sektor.append(b["Activity Sector"])
        segment.append(b["Market Segment"])
    except IndexError:
        print('IndexError')
        continue

df.set_index
301033387.0