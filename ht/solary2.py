import matplotlib.pyplot as plt

# Given data structure
data = {
    "World Class": {"Keeper": 9150, "Defensive": 6930, "Playmaker": 8610, "Passing": 4930, "Winger": 4430, "Scorer": 7770},
    "Divine+1": {"Keeper": 87280, "Defensive": None, "Playmaker": None, "Passing": None, "Winger": None, "Scorer": 91800},
    "Passable": {"Keeper": 830, "Defensive": 270, "Playmaker": 270, "Passing": 250, "Winger": 250, "Scorer": 270},
    "Divine": {"Keeper": 68210, "Defensive": None, "Playmaker": 129150, "Passing": 75100, "Winger": 67660, "Scorer": None},
    "Inadequate": {"Keeper": 610, "Defensive": 250, "Playmaker": 250, "Passing": 250, "Winger": 250, "Scorer": 250},
    "Magnificent": {"Keeper": 6450, "Defensive": 4070, "Playmaker": 5030, "Passing": 2930, "Winger": 2630, "Scorer": 4550},
    "Utopian": {"Keeper": 52990, "Defensive": 75730, "Playmaker": 93180, "Passing": 54680, "Winger": 49380, "Scorer": 84470},
    "Magical": {"Keeper": 40930, "Defensive": 54160, "Playmaker": 66330, "Passing": 39440, "Winger": 35720, "Scorer": 60240},
    "Brilliant": {"Keeper": 4530, "Defensive": 2310, "Playmaker": 2830, "Passing": 1690, "Winger": 1530, "Scorer": 2570},
    "Mythical": {"Keeper": 31480, "Defensive": 38310, "Playmaker": 46640, "Passing": 28200, "Winger": 25650, "Scorer": 42480},
    "Outstanding": {"Keeper": 3170, "Defensive": 1290, "Playmaker": 1550, "Passing": 970, "Winger": 890, "Scorer": 1430},
    "Extra-terrestrial": {"Keeper": 24150, "Defensive": 26840, "Playmaker": 32450, "Passing": 19910, "Winger": 17810, "Scorer": 29650},
    "Formidable": {"Keeper": 2250, "Defensive": 730, "Playmaker": 850, "Passing": 590, "Winger": 550, "Scorer": 790},
    "Titanic": {"Keeper": 18050, "Defensive": 18270, "Playmaker": 22370, "Passing": 12870, "Winger": 11510, "Scorer": 20490},
    "Supernatural": {"Keeper": 12910, "Defensive": 11450, "Playmaker": 14250, "Passing": 8090, "Winger": 7250, "Scorer": 12830},
    "Excellent": {"Keeper": 1590, "Defensive": 450, "Playmaker": 510, "Passing": 390, "Winger": 370, "Scorer": 470},
    "Solid": {"Keeper": 1150, "Defensive": 310, "Playmaker": 330, "Passing": 290, "Winger": 290, "Scorer": 330},
}

# Function to find the minimum value for each level across all skills
def min_value_for_level(level):
    return min(filter(None, data[level].values()))  # Filter out None values and find the minimum

# Sorting levels based on their minimum skill value
sorted_levels_by_min_value = sorted(data.keys(), key=min_value_for_level)

# Update level numbers to reflect the new order
level_numbers_sorted_by_value = {level: i + 7 for i, level in enumerate(sorted_levels_by_min_value)}

# Define skill areas
skill_areas = ["Keeper", "Defensive", "Playmaker", "Passing", "Winger", "Scorer"]

# Plotting the skill progression
plt.figure(figsize=(15, 10))

for skill in skill_areas:
    level_values = [(level_numbers_sorted_by_value[level], data[level].get(skill)) for level in sorted_levels_by_min_value if skill in data[level] and data[level][skill] is not None]
    if level_values:
        levels, values = zip(*level_values)  # Unpacking levels and values
        plt.plot(levels, values, marker='o', label=skill)

plt.title("Skill Progression from Lowest to Highest Values")
plt.xlabel("Skill Level Number")
plt.ylabel("Skill Value")
plt.xticks(list(level_numbers_sorted_by_value.values()), list(level_numbers_sorted_by_value.keys()), rotation=45)
plt.grid(True)
plt.legend()
plt.show()
