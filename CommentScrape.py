import pandas as pd
import praw
import os
from praw.models import MoreComments
import re


os.environ['id'] = "xx"
os.environ['secret'] = "xx"
os.environ['name'] = 'xx'
os.environ['username'] = 'xx'
os.environ['password'] = 'xx'


def getComments(post):
    iden = os.environ['id']
    secret = os.environ['secret']
    name = os.environ['name']
    user = os.environ['username']
    pw = os.environ['password']
    reddit = praw.Reddit(client_id= iden,
                         client_secret=secret,
                         user_agent=name,
                         username=user,
                         password=pw)
    submission = reddit.submission(url=post)

    blank = []
    submission.comments.replace_more(limit=None)
    for top_level_comment in submission.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        if top_level_comment.body == "[deleted]":
            continue
        text = top_level_comment.body
        text = ''.join(e for e in text if e.isalnum() or e==" " or e==".")

        guess = re.findall("\d+\.*\d+",text)
        if guess:
            dict1 = {"userName":top_level_comment.author,"guess":guess[0],"body": text}
        else:
            dict1 = {"userName": top_level_comment.author, "body": text}
        blank.append(dict1)
    df = pd.DataFrame(blank)
    df.to_csv('results.csv',index=False)


if __name__ == "__main__":
    url = "https://old.reddit.com/r/financialindependence/comments/fwnrpt/mod_approvedrfi_contest_guess_what_the_sp500_will/"
    getComments(url)
