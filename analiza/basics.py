
df.info()
df.describe() # distribution of the data, outlayers
df = df.drop_duplicates(keep="first")
df.drop(drop,cols, axis=1)
df.sort_values(by="column", ascending=True).head()
df.columns.replace(" ", "")

#how to find outlayers and remove them

df['col'].idmax()

num_bins = 10
plt.hist(df['col'], num_bins)
sns.displot(df['col'], bins=10)

make_dist = df.groupby('col').size() # count of given category
make_dist.plot(title="make Distribution")
df.heatmap()
sns.boxplot(x="Type", y= "col", data=df)

# outlayers:
z_scores = stats.zscore(df) # scipy.stats.zscore(a) w
# calculate z-scores of `df`

abs_z_scores = np.abs(z_scores)
filtered_entries = (abs_z_scores < 3).all(axis=1)
new_df = df[filtered_entries]