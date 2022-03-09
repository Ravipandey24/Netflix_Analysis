import numpy as np
import pandas as pd
import plotly.express as px
from textblob import TextBlob

df = pd.read_csv("netflix_titles.csv")

# Content Distribution by ratings
z = df.groupby(['rating']).size().reset_index(name="counts")
pieChart = px.pie(z, values='counts', names='rating', title='Distribution of Content Ratings on Netflix',
                  color_discrete_sequence=px.colors.qualitative.Set3)
# pieChart.show()
        #pie chart showing the content distribution percentage based on type-Ratings

#Top Directors and Actors

directors = df["director"].str.split(",", expand=True).stack().to_frame()
directors.rename(columns={0: "Director"}, inplace=True)
                #Forming a directors-only dataframe

director_data = directors.groupby(["Director"]).size().reset_index(name="Total_Content_on_Netflix")
director_data = director_data[director_data.Director != np.nan]
                #Grouping the dataframe and removing the nan values if any

Top_Directors = director_data.sort_values(by=["Total_Content_on_Netflix"], ascending=False).head(10)
                #sorting the dataframe and picking the top 10 values

#Same process for Actors :-

actors = df["cast"].str.split(",", expand=True).stack().to_frame()
actors.rename(columns={0: "Actor"}, inplace=True)

actor_data = actors.groupby(["Actor"]).size().reset_index(name="Total_Content_on_Netflix")
actor_data = actor_data[actor_data.Actor != np.nan]

Top_Actors = actor_data.sort_values(by=["Total_Content_on_Netflix"], ascending=False).head(10)

fig1 = px.bar(Top_Directors, x="Total_Content_on_Netflix", y="Director", title="Top 10 Directors on Netflix")
fig2 = px.bar(Top_Actors, x="Total_Content_on_Netflix", y="Actor", title="Top 10 Actors on Netflix")

fig1.show()
fig2.show()

#Content Analysis - TV show vs Movies over the years

content = df[["type", "release_year"]]
content.rename(columns={"release_year": "Release_Year"}, inplace=True)

content_analyzed = content.groupby(["type", "Release_Year"]).size().reset_index(name="Total_Content")
content_analyzed = content_analyzed[content_analyzed.Release_Year >= 2010]

fig3 = px.line(content_analyzed, x="Release_Year", y="Total_Content", color="type", title="Trend of Content Produced after 2010 on Netflix")
fig3.show()

#Content Analysis - Type of content being produced over the years
  # using TextBlob

content_dis = df[["release_year", "description"]]
content_dis.insert(2, "Sentimental", np.nan)

for index, row in content_dis.iterrows():
    statement = row["description"]
    testimonial = TextBlob(statement)
    p = testimonial.sentiment.polarity

    if p == 0:
        x = "Neutral"

    elif p > 0:
        x = "Negative"

    else:
        x = "Positive"

    content_dis.loc[index, "Sentimental"] = x

content_dis = content_dis.groupby(["release_year", "Sentimental"]).size().reset_index(name="Total_Content")
content_dis = content_dis[content_dis.release_year >= 2010]

fig4 = px.bar(content_dis, x="release_year", y="Total_Content", color="Sentimental", title = "Sentiment of title on Netflix after 2010")
fig4.show()

