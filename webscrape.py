from psaw import PushshiftAPI
import datetime as dt
import pandas as pd
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
        dates.append(submission.created_utc)
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
""" 
#clean tickers
tickersClean = []
regex = re.compile('[^a-zA-Z]')
#clean each ticker
for ticker in tickersUpper:
    clean = regex.sub('', ticker)
    #If there is still text after the ticker (as tickers have a max length of 4), include only the ticker.
    if len(clean) > 4:
        clean = clean[:4]
    #append only if the ticker is not an empty string
    if len(clean) != 0:
        tickersClean.append(clean) """

#convert lists into CSV file
dict = {"ticker": tickersUpper, "dates": datesUpper, "title": titlesUpper, "url": urlsUpper}
df = pd.DataFrame(dict)
df.to_csv("wsb.csv")
