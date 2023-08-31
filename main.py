# -*- coding: utf-8 -*-
"""CSE 351 HW1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JsOPLhzoYK-9EnbmYOQPtckSa6WYHDMk
"""

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

df = pd.read_csv("drive/MyDrive/AB_NYC_2019.csv")
df.head()

df.describe()

len(df)

"""##Task 1
###Use the built-in function dropna() in pandas to drop rows which contain invalid data (row that contains at least one null value)
###In addition, we consider rows to be invalid if the price or availability equal to 0.

"""

df = df.dropna()
df = df[df["price"] > 0]
df = df[df["availability_365"] > 0]

"""##Task 2

###part a
####Find Top 5 and Bottom 5 neighborhood based on the price of the Airbnb in that neighborhood
"""

# select only neighborhoods with more than 5 listings
neighbourhood_count = df["neighbourhood"].value_counts()
target_neighbourhood = neighbourhood_count[neighbourhood_count > 5]
target_df = df[df["neighbourhood"].isin(target_neighbourhood.index)]

# prices_by_neighbourhood contains the mean prices of each neighborhood in descending order.
prices_by_neighbourhood = target_df.groupby("neighbourhood").mean()["price"].sort_values(ascending = False)
print(prices_by_neighbourhood)

top_5_neighbourhood = prices_by_neighbourhood[:5] # top 5 neighborhoods with the highest mean prices.
bottom_5_neighbourhood = prices_by_neighbourhood[len(prices_by_neighbourhood)-5:] # bottom 5 neighborhoods with the lowest mean prices.

"""#### top 5 neighborhood based on price"""

print(top_5_neighbourhood)

"""#### bottom 5 neighborhood based on price"""

print(bottom_5_neighbourhood)

"""###part b
####According to the graph, there is a significant difference in price variation among various neighborhoods.

####- Manhattan has the highest average price at $195.94, which is significantly higher than the other boroughs.

####- The Bronx has the lowest average price at $80.75
"""

df.groupby("neighbourhood_group").mean()[["price"]]

ax = df.groupby("neighbourhood_group").mean()["price"].plot(kind="bar")
plt.xticks(rotation=0)
plt.ylabel("Price")
plt.xlabel("Neighbourhood Group")
# plt.gcf().set_dpi(150)
plt.title("Average Airbnb Listing Price by Neighbourhood Group")

for i, v in enumerate(df.groupby("neighbourhood_group").mean()["price"]):
    ax.text(i, v, "${:.2f}".format(v), ha='center', va='bottom', fontweight='bold')


overall_avg_price = df['price'].mean()

plt.tight_layout()


plt.show()

"""## Task 3

####The most positive correlation is calculated_host_listings_count and availability_365. The most negative correlation is minimum_nights and number_of_reviews.
"""

corr = df[["minimum_nights", "number_of_reviews", "calculated_host_listings_count", "availability_365", "price"]].corr(method="pearson")
corr

sns.heatmap(corr, cmap='coolwarm', annot=True, center=0)
plt.show()

"""##Task 4

### part a
"""

sns.scatterplot(data=df, x=df["longitude"], y=df["latitude"], hue=df["neighbourhood_group"])

plt.show()

"""### part b

####According to the plot, Manhattan neighborhood group is most expensive
"""

df_less_than_1000 = df[df["price"] <= 1000]

sns.scatterplot(data=df_less_than_1000, x=df_less_than_1000["longitude"], y=df_less_than_1000["latitude"], hue=df_less_than_1000["price"])

plt.show()

"""## Task 5"""

text = ' '.join([str(n) for n in df["name"]])

wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate(text)

plt.figure(figsize=(8,8))
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

plt.show()

"""## Task 6

####Eastchester has the busiest host
"""

unique_hosts_df = df.drop_duplicates(subset=["host_id"])

host_listing_by_neighbourhood = unique_hosts_df.groupby("neighbourhood").mean().pivot_table(index='neighbourhood')["calculated_host_listings_count"].sort_values(ascending=False)
host_listing_by_neighbourhood

df_top_5_listings = unique_hosts_df.sort_values("calculated_host_listings_count", ascending=False).head(5)
df_busiest_5_hosts = df[df["host_id"].isin(df_top_5_listings["host_id"])]

"""####Price - The top 5 busiest hosts charge a higher price compared to the average host, which could potentially make their properties less appealing to prospective renters and result in a longer duration on the market."""

ax = sns.boxplot(data = [list(df_busiest_5_hosts["price"]), list(df["price"])], showfliers=False)
ax.set_ylabel("Price")
ax.set_title("Price of Top 5 Busiest Airbnb Hosts vs All Hosts")

ax.set_xticklabels(["Top 5 Busiest Airbnb Hosts", "All Hosts"])

plt.show()

"""####minimum_nights - The top 5 busiest hosts have a much higher minimum-night requirement compared to the average host, which may make their properties less desirable to potential renters who are not interested in renting for a long period of time. As a result, their listings may stay on the market for a longer duration.

"""

median_top_5_hosts = df_busiest_5_hosts["minimum_nights"].median()
median_entire_dataset = df["minimum_nights"].median()

fig, ax = plt.subplots()
bars = ax.bar(['Top 5 Busiest Hosts Listings', 'Entire Dataset'], [median_top_5_hosts, median_entire_dataset])

ax.set_ylabel('Minimum Nights')

ax.set_title('Median Minimum Nights by Hosts')

for i, bar in enumerate(bars):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{int(bar.get_height())}",
            ha='center', va='bottom', fontsize=10)

plt.show()

"""## Task 7

#### The pie chart depicts that the market is dominated by entire home/apartment listings, whereas shared rooms have the smallest market share. Therefore, if someone plans to become an Airbnb host in the future, it would be advisable for them to avoid listing a shared room.
"""

roomtype_series = df["room_type"].value_counts()
fig, ax = plt.subplots(figsize=(8, 6))
ax = roomtype_series.plot(kind="pie",labels=None, autopct='%1.1f%%')
ax.set_title('Room Type', horizontalalignment='center')
ax.set_ylabel("")
ax.legend(labels=roomtype_series.index, bbox_to_anchor=(1, 0.5))
plt.show()

"""#### The pie chart provides a clear illustration of how Airbnb hosts are distributed across the various neighborhoods in New York City. The largest proportion of hosts is from Manhattan, accounting for 41.9% of the total, while Brooklyn comes in second with 41.6%."""

neighbourhood_group_series = unique_hosts_df["neighbourhood_group"].value_counts()
fig, ax = plt.subplots(figsize=(8, 6))
ax = neighbourhood_group_series.plot(kind="pie",labels=None, autopct='%1.1f%%')
ax.set_title('Distribution of Airbnb Hosts across NYC Neighbourhoods', horizontalalignment='center')
ax.set_ylabel("")
ax.legend(labels=neighbourhood_group_series.index, bbox_to_anchor=(1, 0.5))
plt.show()