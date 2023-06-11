"""
NovaScotiansBotConfig

    This file should contain all your private variables required to use:
        -Reddit Account     @ https://www.Reddit.com
        -Reddit API         @ https://www.Reddit.com/prefs/apps/
        -MediaStack API     @ https://www.MediaStack.com
        -TheNewsAPI API     @ https://www.TheNewsAPI.com
        -TheGuardian API    @ https://Open-Platform.TheGuardian.com/
        -GNews API          @ https://GNews.io/

    All ./APIs/*.py files will search this file for the private data they require. So, if any of their
    related fields are blank '', that specific code will not attempt an API call.

    You can leave blank fields to test, or to skip over a specific API you don't want to use.

    Source:
        https://github.com/xTkAx/NovaScotiansBot

"""

# region Reddit:

# region Reddit Account
# @ https://www.Reddit.com:

REDDIT_USERNAME = 'NovaScotiansBot'

REDDIT_PASSWORD = ''

REDDIT_SUBREDDIT = 'NovaScotians'

# endregion Reddit Account

# region Reddit API
# @ https://www.Reddit.com/prefs/apps/:
REDDIT_CLIENT_ID = ''

REDDIT_CLIENT_SECRET = ''

REDDIT_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'

# endregion Reddit API

# endregion Reddit

# region News APIs:

# @ https://www.MediaStack.com:
MEDIASTACK_API_KEY = ''

# @ https://www.TheNewsAPI.com:
THENEWSAPI_API_KEY = ''

# @ https://Open-Platform.TheGuardian.com/:
THEGUARDIAN_API_KEY = ''

# @ https://GNews.io/:
GNEWS_API_KEY = ''

# endregion News APIs
