import praw
from psaw import PushshiftAPI

api = PushshiftAPI()
reddit = praw.Reddit(
    client_id = "client_id",
    client_secret = "client_secret",
    username = "username",
    password = "password",
    user_agent = "user_agent"
)

subreddits = ['wallstreetbets']
start_year = 2020
end_year = 2020

basecorpus = 'Webmining/'

import time
def log_action(action):
    print(action)
    return

import os
import pandas as pd
import datetime as dt


for year in range(start_year, end_year + 1):
    action = "[Year] " + str(year)
    log_action(action)

    dirpath = basecorpus + str(year)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    ts_after = int(dt.datetime(2020, 6, 10).timestamp())
    ts_before = int(dt.datetime(2020, 6, 17).timestamp())


    for subreddit in subreddits:
        start_time = time.time()

        action = "\t[Subreddit] " + subreddit
        log_action(action)

        subredditdirpath = dirpath + '/' + subreddit
        if os.path.exists(subredditdirpath):
            continue
        else:
            os.makedirs(subredditdirpath)

        submissions_csv_path = str(year) + '-' + subreddit + '-submissions.csv'


        submissions_dict = {
            "id": [],
            "url": [],
            "title": [],
            "score": [],
            "num_comments": [],
            "created_utc": [],
            "selftext": [],
            "name": [],
            "author": [],
            "link_flair_css_class": [],
            "link_flair_text": [],
        }


        gen = api.search_submissions(
            after=ts_after,
            before=ts_before,
            filter=['id'],
            subreddit=subreddit,
        )


        for submission_psaw in gen:
            # Selecting which atributes of the posts i want to download
            submission_id = submission_psaw.d_['id']
            submission_praw = reddit.submission(id=submission_id)

            submissions_dict["id"].append(submission_praw.id)
            submissions_dict["url"].append(submission_praw.url)
            submissions_dict["title"].append(submission_praw.title)
            submissions_dict["score"].append(submission_praw.score)
            submissions_dict["num_comments"].append(submission_praw.num_comments)
            submissions_dict["created_utc"].append(submission_praw.created_utc)
            submissions_dict["selftext"].append(submission_praw.selftext)
            submissions_dict["name"].append(submission_praw.name)
            submissions_dict["author"].append(submission_praw.author)
            submissions_dict["link_flair_css_class"].append(submission_praw.link_flair_css_class)
            submissions_dict["link_flair_text"].append(submission_praw.link_flair_text)

            print(submission_praw.id)

        # single csv file with all submissions
        pd.DataFrame(submissions_dict).to_csv(subredditdirpath + '/' + submissions_csv_path,
                                              index=False)

        action = f"\t\t[Info] Found submissions: {pd.DataFrame(submissions_dict).shape[0]}"
        log_action(action)

        action = f"\t\t[Info] Elapsed time: {time.time() - start_time: .2f}s"
        log_action(action)
