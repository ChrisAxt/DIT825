import datetime
from datetime import timedelta
from newsapi import NewsApiClient

# use pandas to create dataframe
import pandas as pd

# get today's date
dateToday = datetime.datetime.today()

daysOfPull = 30

# minus 20 days from the date
startDate = dateToday - timedelta(days=daysOfPull)

# Get data from NEWS API

# Init
newsapi = NewsApiClient(api_key='913098f1a0fd429a88cee464f86f2201')

data = []
for i in range(20):
    dateToUse = startDate + timedelta(days=i)
    date = dateToUse.strftime("%Y-%m-%d")
    all_articles = newsapi.get_everything(sources='breitbart-news,fox-news,msnbc,reuters,the-huffington-post,the-verve,bbc',from_param=date,to=date,language='en',sort_by='relevancy',page=5)
    data.append(all_articles['articles'])

    convertedData = []
for i in range(len(data)):
    for j in range(len(data[i])):
        convertedData.append({"sentence": data[i][j]['description'], "pub_year": data[i][j]['publishedAt'][0:4], "news_link": data[i][j]['url'], "outlet" : data[i][j]['source']['name']})
        # convertedData.append(data[i]['articles'][0])

df = pd.DataFrame(convertedData)
df.head()