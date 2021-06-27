from psaw import PushshiftAPI
import datetime as dt
import pandas as pd

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

#convert lists into CSV file
dict = {"Ticker Symbol": tickers, "Date": dates, "Title": titles}
df = pd.DataFrame(dict)
df.to_csv("wsb.csv")