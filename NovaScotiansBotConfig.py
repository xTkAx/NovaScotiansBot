"""
NovaScotiansBotConfig

    This file contains private variables required to use:
        -Reddit
        -Praw Reddit API
        -MediaStack API
        -TheNewsAPI API
        -TheGuardian API

    All APIs will check this data, so if any of its related fields are blank '',
    that specific API will not be used.

    Source:
        https://github.com/xTkAx/NovaScotiansBot

"""

# region RedditAPI:

REDDIT_CLIENT_ID = ''

REDDIT_CLIENT_SECRET = ''

REDDIT_USERNAME = 'NovaScotiansBot'

REDDIT_PASSWORD = ''

REDDIT_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'

REDDIT_SUBREDDIT = 'NovaScotians'

# endregion RedditAPI

# region NEWS API KEYS:

MEDIASTACK_API_KEY = ''

THENEWSAPI_API_KEY = ''

THEGUARDIAN_API_KEY = ''

# endregion NEWS API KEYS
