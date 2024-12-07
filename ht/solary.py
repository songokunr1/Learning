import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Given data structure
data = {
    "World Class": {"Keeper": 9150, "Defensive": 6930, "Playmaker": 8610, "Passing": 4930, "Winger": 4430,
                    "Scorer": 7770},
    "Divine+1": {"Keeper": 87280, "Defensive": None, "Playmaker": None, "Passing": None, "Winger": None,
                 "Scorer": 91800},
    "Passable": {"Keeper": 830, "Defensive": 270, "Playmaker": 270, "Passing": 250, "Winger": 250, "Scorer": 270},
    "Divine": {"Keeper": 68210, "Defensive": None, "Playmaker": 129150, "Passing": 75100, "Winger": 67660,
               "Scorer": None},
    "Inadequate": {"Keeper": 610, "Defensive": 250, "Playmaker": 250, "Passing": 250, "Winger": 250, "Scorer": 250},
    "Magnificent": {"Keeper": 6450, "Defensive": 4070, "Playmaker": 5030, "Passing": 2930, "Winger": 2630,
                    "Scorer": 4550},
    "Utopian": {"Keeper": 52990, "Defensive": 75730, "Playmaker": 93180, "Passing": 54680, "Winger": 49380,
                "Scorer": 84470},
    "Magical": {"Keeper": 40930, "Defensive": 54160, "Playmaker": 66330, "Passing": 39440, "Winger": 35720,
                "Scorer": 60240},
    "Brilliant": {"Keeper": 4530, "Defensive": 2310, "Playmaker": 2830, "Passing": 1690, "Winger": 1530,
                  "Scorer": 2570},
    "Mythical": {"Keeper": 31480, "Defensive": 38310, "Playmaker": 46640, "Passing": 28200, "Winger": 25650,
                 "Scorer": 42480},
    "Outstanding": {"Keeper": 3170, "Defensive": 1290, "Playmaker": 1550, "Passing": 970, "Winger": 890,
                    "Scorer": 1430},
    "Extra-terrestrial": {"Keeper": 24150, "Defensive": 26840, "Playmaker": 32450, "Passing": 19910, "Winger": 17810,
                          "Scorer": 29650},
    "Formidable": {"Keeper": 2250, "Defensive": 730, "Playmaker": 850, "Passing": 590, "Winger": 550, "Scorer": 790},
    "Titanic": {"Keeper": 18050, "Defensive": 18270, "Playmaker": 22370, "Passing": 12870, "Winger": 11510,
                "Scorer": 20490},
    "Supernatural": {"Keeper": 12910, "Defensive": 11450, "Playmaker": 14250, "Passing": 8090, "Winger": 7250,
                     "Scorer": 12830},
    "Excellent": {"Keeper": 1590, "Defensive": 450, "Playmaker": 510, "Passing": 390, "Winger": 370, "Scorer": 470},
    "Solid": {"Keeper": 1150, "Defensive": 310, "Playmaker": 330, "Passing": 290, "Winger": 290, "Scorer": 330},
}

# Convert the data dictionary into a DataFrame and transpose it
df = pd.DataFrame(data).transpose()

# Assign skill levels starting from 5 for 'Inadequate' and incrementing by 1 for each level
skill_levels = {level: i + 5 for i, level in
                enumerate(sorted(data.keys(), key=lambda x: data[x].get('Keeper', float('inf'))))}

# Map the skill levels to a new column in the DataFrame
df['skill_level'] = df.index.map(skill_levels)


# Function to apply the computation
def apply_computation(row, df):
    # x is the current row's 'skill_level'
    x = row['skill_level']
    # Find the previous row based on 'skill_level'
    previous_row = df[df['skill_level'] == x - 1]

    if not previous_row.empty:
        x_minus_1 = previous_row.iloc[0]['Keeper']
        return (row['Keeper'] - x_minus_1) / x_minus_1
    else:
        return None


# Apply the computation to a new column 'computed_value'
df['computed_value'] = df.apply(apply_computation, df=df, axis=1)

# Display the DataFrame
# Replace None values with NaN for calculations
df.fillna(value=np.nan, inplace=True)
skill_areas = ["Keeper", "Defensive", "Playmaker", "Passing", "Winger", "Scorer"]

for skill in skill_areas:
    plt.plot(df.skill_level, df[skill], marker='o', label=skill)

plt.title("Skill Progression and Computed Values")
plt.xlabel("Skill Level")
plt.ylabel("Value")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.show()
