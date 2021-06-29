from psaw import PushshiftAPI
import datetime as dt
import pandas as pd
import re

api = PushshiftAPI()

start_epoch = int(dt.datetime(2021, 6, 25).timestamp())

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

#convert tickers to all uppercase
tickersUpper = []
for tickerList in tickers:
    for ticker in tickerList:
        tickersUpper.append(ticker.upper())

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
        tickersClean.append(clean)

#convert lists into CSV file
#The current implementation cleans the tickers before putting it into a dataframe, which causes an issue when combining it with the dates and titles lists due to their different lengths.
#dict = {"Ticker": tickersClean, "Date": dates, "Title": titles} 
dict = {"Ticker": tickersClean}
df = pd.DataFrame(dict)
df.to_csv("wsb.csv")
