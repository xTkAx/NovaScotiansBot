"""
RedditAPI

    This script contains the methods used to post data to https://www.Reddit.com/

"""
import praw
from AccountConfiguration.AccountConfig import CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD, USER_AGENT, SUBREDDIT


def post_article(title, url):
    # Define praw Reddit object:
    r = praw.Reddit(client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    username=USERNAME,
                    password=PASSWORD,
                    user_agent=USER_AGENT)

    # Define the subreddit:
    subreddit = r.subreddit(SUBREDDIT)

    # Try to post the article or throw on error:
    try:
        subreddit.submit(title, url=url)
    except Exception as e:
        raise ValueError(e)
