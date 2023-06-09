"""
RedditAPI

    This script contains the methods used to post data to https://www.Reddit.com/

    Documentation: https://praw.readthedocs.io/en/stable/index.html

"""
import praw
from NovaScotiansBotConfig import CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD, USER_AGENT, SUBREDDIT


def __define_praw_reddit_object():
    # Define praw Reddit object:
    r = praw.Reddit(client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    username=USERNAME,
                    password=PASSWORD,
                    user_agent=USER_AGENT)
    return r


def post_article(title, url):
    praw = __define_praw_reddit_object()

    # Try to post the article or throw on error:
    try:
        praw.subreddit(SUBREDDIT).submit(title, url=url)
    except Exception as e:
        raise ValueError(e)


def create_new_monthly_lounge(lounge_title, lounge_description):
    # First prefix the title:
    lounge_title = f'r/{SUBREDDIT} {lounge_title}'

    # Get the praw object to work with reddit:
    praw = __define_praw_reddit_object()

    # Define the NovaScotiaBot username as uppercase:
    upper_username = USERNAME.upper()

    # Define a variable to hold the old_lounge_sticky id:
    old_lounge_sticky_id = ''

    # Subreddits can only have 2 stickies, so lets check sticky 1 and then 2, and catch if it fails on any:
    try:
        if praw.submission(praw.subreddit(SUBREDDIT).sticky(1).id).author.name.upper() == upper_username:
            old_lounge_sticky_id = praw.subreddit(SUBREDDIT).sticky(1).id
            print(f'Found current Lounge sticky ID: {old_lounge_sticky_id}')
        elif praw.submission(praw.subreddit(SUBREDDIT).sticky(2).id).author.name.upper() == upper_username:
            old_lounge_sticky_id = praw.subreddit(SUBREDDIT).sticky(2).id
            print(f'Found current Lounge sticky ID: {old_lounge_sticky_id}')
    except Exception as e:
        print(f'Problem searching stickies: [ {e} ]')

    # If the old_lounge_sticky_id was found:
    if old_lounge_sticky_id != '':
        try:
            submission = praw.submission(old_lounge_sticky_id)
            suppress_screen_text = submission.mod.sticky(False, False)
            print(f'Unstickied old Lounge sticky ID: {old_lounge_sticky_id}')
            # Append lounge_description with a link to the last Chat Lounge:
            #lounge_description = f'{lounge_description}\r\n[Last month\'s Chat Lounge]' \
            #                     f'(https://reddit.com/r/{SUBREDDIT}/comments/{old_lounge_sticky_id}/)'
        except Exception as e:
            print(f'Could not unsticky Lounge sticky: [ {e} ]')
    else:
        print(f'No Lounge sticky ID\'s found from user: {USERNAME}.\r\n[ {e} ]')

    # Try post the new Lounge post:
    try:
        new_lounge_post = praw.subreddit(SUBREDDIT).submit(lounge_title,
                                                           selftext=lounge_description,
                                                           url=None,
                                                           flair_id=None,
                                                           flair_text=None,
                                                           resubmit=True,
                                                           send_replies=True,
                                                           nsfw=False,
                                                           spoiler=False,
                                                           collection_id=None,
                                                           discussion_type='CHAT')
        # Sticky the Lounge post:
        praw.submission(new_lounge_post.id).mod.sticky()
        print(f'Posted new Lounge post ID: {new_lounge_post.id}.')
    except Exception as e:
        raise ValueError(e)
