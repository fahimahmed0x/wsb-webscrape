from psaw import PushshiftAPI
import datetime as dt
import pandas as pd
import numpy as np
import re

api = PushshiftAPI()

year = int(input("Enter a year (ex. 2021): "))
month = int(input("Enter a month (ex. 6): "))
day = int(input("Enter a day (ex. 28): "))

start_epoch = int(dt.datetime(year, month, day).timestamp())

submissions = api.search_submissions(after = start_epoch,
                                     subreddit = "wallstreetbets",
                                     filter = ["url", "author", "title", "subreddit"])

tickers = []
dates = []
titles = []
urls = []

for submission in submissions:
    words = submission.title.split()
    #look for any word that starts with a $, and does not contain any digits.
    cashtags = list(set(filter(lambda word: word.lower().startswith("$") and any(char.isdigit() for char in word) == False, words)))

    #append to list if there is a cashtag
    if len(cashtags) > 0:
        tickers.append(cashtags)
        dates.append(submission.created_utc) #unix timestamp
        titles.append(submission.title)
        urls.append(submission.url)


#convert tickers to all uppercase, and do the same with the other lists to keep the data in similar structures 
tickersUpper = []
datesUpper = []
titlesUpper = []
urlsUpper = []
for tickerList in tickers:
    i = int(tickers.index(tickerList))
    for ticker in tickerList:
        tickersUpper.append(ticker.upper())
        #append the dates, titles, and url, for each of the tickers mentioned in the post title.
        datesUpper.append(dates[i])
        titlesUpper.append(titles[i])
        urlsUpper.append(urls[i])

#convert lists into dataframe
dict = {"ticker": tickersUpper, "date": datesUpper, "title": titlesUpper, "url": urlsUpper}
df = pd.DataFrame(dict)

#clean tickers in dataframe
df["ticker"].replace('[^a-zA-Z]', '', regex = True, inplace = True) #remove anything that's not a letter
df["ticker"] = df["ticker"].str[:4] #tickers have a max length of 4 strings
df["ticker"] = df["ticker"].str.upper() #capitalize tickers
df["ticker"].replace('', np.nan, inplace = True) #convert empty strings into NaN...
df.dropna(subset=["ticker"], inplace=True) #... and drop them

df.to_csv("wsb.csv")
