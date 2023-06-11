"""
GNewsAPI

    This file contains the methods used to pull data from https://gnews.io/
    -100 free searches a day.
    -Must be url-encoded.
    -Example url to search for news articles:
    https://gnews.io/api/v4/search?q=example&apikey={GNEWS_API_KEY}&q={search}&from={date}T00:00:00Z&sortby=publishedAt&in=title,description,content&lang=en

    Documentation:
        https://gnews.io/docs/v4#introduction

    Source:
        https://github.com/xTkAx/NovaScotiansBot

"""
# region Libraries:
import requests
from datetime import datetime
from NovaScotiansBotConfig import GNEWS_API_KEY

# endregion Libraries

# region Methods:

# region confirm_user_config():
"""
    This method confirm the user filled all the data in NovaScotiansBotConfig.

    Parameters:
        None.

    Returns:
        [True] or [False] depending on if the user filled all the values.

"""


def confirm_user_config():
    if GNEWS_API_KEY == '':
        return False
    else:
        return True


# endregion confirm_user_config()

# region get_news()
"""
    This method will generate the query to get the news from GNews, and yield each article back to the caller
     (or will throw an error).

    Parameters:
        search_string:      The search string to query the API with.

    Yields:
        Articles of data in the format:
            ['', title, url]

    Throws:
        Error

"""


def get_news(search_string):
    # If the user filled all fields in NovaScotiansBotConfig:
    if confirm_user_config():

        # Clean the search_string as required for this API (%22 = '"', %20 = ' '):
        search_string = f'%22{search_string.strip().replace(" ", "%20")}%22'

        # Get today's date for the search:
        date_pattern = f'{datetime.now().year}-{datetime.now().month:02d}-{datetime.now().day:02d}T00:00:00Z'

        # Create the url to request the data from GNews (%2C = ,)
        request_url = f'https://gnews.io/api/v4/search' \
                      f'?apikey={GNEWS_API_KEY}' \
                      f'&q={search_string}' \
                      f'&from={date_pattern}' \
                      f'&sortby=publishedAt' \
                      f'&in=title,description%2Ccontent' \
                      f'&lang=en'

        # Try to get the json from the request or throw an error:
        try:
            results = requests.get(request_url).json()

            # Access the 'articles' in the json:
            json_data = results['articles']

            # Loop through each element of the json data:
            for i in range(len(json_data)):
                block = json_data[i]

                # Get the 'title' and 'url':
                title = block['title']
                url = block['url']

                # Yield the article to the caller:
                yield ['', title, url]

        except Exception as get_news_e:
            raise ValueError(f'GNewsAPI/get_news exception: {get_news_e}')

    else:
        raise ValueError(f'Empty fields were found in NovaScotiansBotConfig for GNewsAPI')
# endregion get_news()

# endregion Methods
