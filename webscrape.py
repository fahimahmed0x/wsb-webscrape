from psaw import PushshiftAPI
import datetime as dt

api = PushshiftAPI()

start_epoch = int(dt.datetime(2021, 6, 25).timestamp())

submissions = api.search_submissions(after = start_epoch,
                                     subreddit = "wallstreetbets",
                                     filter = ["url", "author", "title", "subreddit"])

for submission in submissions:
    words = submission.title.split()
    #look for any word that starts with a $, and does not contain any digits.
    cashtags = list(set(filter(lambda word: word.lower().startswith("$") and any(char.isdigit() for char in word) == False, words)))

    #print if there is a cashtag
    if len(cashtags) > 0:
        print(cashtags)
        print(submission.created_utc)
        print(submission.title)
        print(submission.url)

