"""
TheNewsAPI

    This file contains the methods used to pull data from https://TheNewsAPI.com/
    -Can only pull 3 articles with the free account.
    -Example url to search for news articles:
    api.thenewsapi.com/v1/news/all?api_token={THENEWSAPI_API_KEY}&search={search_string}&published_on={date}&language=en

    Documentation:
        https://www.thenewsapi.com/documentation

    Source:
        https://github.com/xTkAx/NovaScotiansBot

"""
# region Libraries:
import requests
from datetime import datetime
from NovaScotiansBotConfig import THENEWSAPI_API_KEY

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
    if THENEWSAPI_API_KEY == '':
        return False
    else:
        return True


# endregion confirm_user_config()

# region get_news()
"""
    This method will generate the query to get the news from TheNewsAPI.com, and yield each article back to the caller
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

        # Clean the search_string as required for this API:
        search_string = f'%22{search_string.strip().replace(" ", "%20")}%22'

        # Get today's date for the search
        date_pattern = f'{datetime.now().year}-{datetime.now().month:02d}-{datetime.now().day:02d}'

        # Create the url to request the data from TheNewsAPI:
        request_url = f'https://api.thenewsapi.com/v1/news/all' \
                      f'?api_token={THENEWSAPI_API_KEY}' \
                      f'&search={search_string}' \
                      f'&published_on={date_pattern}' \
                      f'&language=en'

        # Try to get the json from the request or throw an error:
        try:
            results = requests.get(request_url).json()
        except Exception as get_news_e:
            raise ValueError(f'TheNewsAPI/get_news exception: {get_news_e}')

        # Access the 'data' in the json:
        json_data = results['data']

        # Loop through each element of the json data:
        for i in range(len(json_data)):
            block = json_data[i]

            # Get the 'title' and 'url':
            title = block['title']
            url = block['url']

            # Yield the article to the caller:
            yield ['', title, url]

    else:
        raise ValueError(f'Empty fields were found in NovaScotiansBotConfig for TheNewsAPI')
# endregion get_news()

# endregion Methods
