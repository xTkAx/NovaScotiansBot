"""
RedditAPI

    This file contains the methods used to post data to https://www.Reddit.com/

    Documentation:
        https://praw.readthedocs.io/en/stable/index.html

    Source:
        https://github.com/xTkAx/NovaScotiansBot

"""
# region Libraries:
import praw
from NovaScotiansBotConfig import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD, \
    REDDIT_USER_AGENT, REDDIT_SUBREDDIT

# endregion Libraries

# region Methods:

# region __define_praw_reddit_object():
"""
    This private method will initialize and return a praw object for other methods to use
    to interface with Reddit.
    
    Parameters:
        None.

    Returns:
        A praw object to interface with reddit.

"""


def __define_praw_reddit_object():
    # Define praw Reddit object:
    r = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                    client_secret=REDDIT_CLIENT_SECRET,
                    username=REDDIT_USERNAME,
                    password=REDDIT_PASSWORD,
                    user_agent=REDDIT_USER_AGENT)
    return r


# endregion __define_praw_reddit_object():

# region confirm_user_config():
"""
    This method confirm the user filled all the data in NovaScotiansBotConfig.

    Parameters:
        None.

    Returns:
        [True] or [False] depending on if the user filled all the values.

"""


def confirm_user_config():
    if REDDIT_CLIENT_ID == '' or REDDIT_CLIENT_SECRET == '' or REDDIT_USERNAME == '' or \
            REDDIT_PASSWORD == '' or REDDIT_USER_AGENT == '' or REDDIT_SUBREDDIT == '':
        return False
    else:
        return True


# endregion confirm_user_config()

# region post_article_to_reddit():
"""
    This method will attempt to post an article to Reddit.
    
    Parameters:
        title:          The title of the article.
        url:            The url of the article

    Returns:
        None.
        
    Throws:
        Error.

"""


def post_article_to_reddit(title, url):
    # If the user filled all fields in NovaScotiansBotConfig:
    if confirm_user_config():

        # Get the praw object:
        post = __define_praw_reddit_object()

        try:  # Post the article:
            post.subreddit(REDDIT_SUBREDDIT).submit(title, url=url)

        except Exception as post_article_e:
            raise ValueError(f'RedditAPI/post_article exception: {post_article_e}')

    else:
        raise ValueError(f'Empty fields were found in NovaScotiansBotConfig for RedditAPI')


# endregion post_article_to_reddit():

# region cycle_to_new_monthly_chat_lounge():
"""
    This method will attempt to cycle to a new monthly Chat Lounge

    Parameters:
        lounge_title:   The title of the article.
        lounge_body:    The body of the article.

    Returns:
        None.

    Throws:
        Error.

"""


def cycle_to_new_monthly_chat_lounge(lounge_title, lounge_body):
    # If the user filled all fields in NovaScotiansBotConfig:
    if confirm_user_config():

        # Get the praw object to work with reddit:
        cl = __define_praw_reddit_object()

        # Prefix the subreddit to the title:
        lounge_title = f'r/{REDDIT_SUBREDDIT} {lounge_title}'

        # Define the NovaScotiaBot username as uppercase:
        upper_username = REDDIT_USERNAME.upper()

        # Define a variable to hold the old_lounge_sticky id:
        old_lounge_sticky_id = ''

        try:  # Find the last month's sticky (note: subreddits can only have 2 stickies):
            # If sticky post 1 matches the upper_username:
            if cl.submission(cl.subreddit(REDDIT_SUBREDDIT).sticky(1).id).author.name.upper() == upper_username:
                # Set the id:
                old_lounge_sticky_id = cl.subreddit(REDDIT_SUBREDDIT).sticky(1).id

            # If sticky post 2 matches the upper_username:
            elif cl.submission(cl.subreddit(REDDIT_SUBREDDIT).sticky(2).id).author.name.upper() == upper_username:
                # Set the id:
                old_lounge_sticky_id = cl.subreddit(REDDIT_SUBREDDIT).sticky(2).id

            # If the Chat Lounge sticky ID is found show it:
            if old_lounge_sticky_id != '':
                print(f'\t\tFound current Chat Lounge sticky ID: {old_lounge_sticky_id}')

        except Exception as cycle_to_new_monthly_chat_lounge_e:
            raise ValueError(f'RedditAPI/cycle_to_new_monthly_chat_lounge() exception:' +
                             f'{cycle_to_new_monthly_chat_lounge_e}')

        # If the old_lounge_sticky_id was found:
        if old_lounge_sticky_id != '':
            try:  # To unstick it:
                submission = cl.submission(old_lounge_sticky_id)

                suppress_screen_text = submission.mod.sticky(False, False)  # Suppressing screen text from this call.

                print(f'\t\tUnstuck old Chat Lounge sticky ID: {old_lounge_sticky_id}')

                # Append a link to lounge_body, so it can link to the Chat Lounge that was just unstuck:
                lounge_body = f'{lounge_body}\r\n[Last month\'s Chat Lounge]' \
                              f'(https://www.reddit.com/r/{REDDIT_SUBREDDIT}/comments/{old_lounge_sticky_id}/)'

            except Exception as cycle_to_new_monthly_chat_lounge_e:
                raise ValueError(f'RedditAPI/cycle_to_new_monthly_chat_lounge() exception:' +
                                 f'{cycle_to_new_monthly_chat_lounge_e}')
        else:
            print(f'\t\tNo Chat Lounge sticky ID\'s were found belonging to u/{REDDIT_USERNAME}.')

        try:  # Post the new Chat Lounge:
            new_lounge_post = cl.subreddit(REDDIT_SUBREDDIT).submit(lounge_title,
                                                                    selftext=lounge_body,
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
            cl.submission(new_lounge_post.id).mod.sticky()

            print(f'\t\tPosted new Chat Lounge post ID: {new_lounge_post.id}.')

        except Exception as cycle_to_new_monthly_chat_lounge_e:
            raise ValueError(f'RedditAPI/cycle_to_new_monthly_chat_lounge() exception: ' +
                             f'{cycle_to_new_monthly_chat_lounge_e}')

    else:
        raise ValueError(f'Empty fields were found in NovaScotiansBotConfig for RedditAPI')

# endregion cycle_to_new_monthly_chat_lounge():

# endregion Methods
