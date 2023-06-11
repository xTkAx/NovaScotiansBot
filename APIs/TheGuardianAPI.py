"""
TheGuardianAPI

    This file contains the methods used to pull data from https://open-platform.theguardian.com/ | guardianapis.com
    -Example url to search for news articles:
    https://content.guardianapis.com/search?api-key={THEGUARDIAN_API_KEY}&q={search}&from-date={date}&lang=en

    Documentation:
        http://open-platform.theguardian.com/documentation/

    Source:
        https://github.com/xTkAx/NovaScotiansBot

"""
# region Libraries:
import requests
from datetime import datetime
from NovaScotiansBotConfig import THEGUARDIAN_API_KEY

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
    if THEGUARDIAN_API_KEY == '':
        return False
    else:
        return True


# endregion confirm_user_config()

# region get_news()
"""
    This method will generate the query to get the news from The Guardian, and yield each article back to the caller
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
        date_pattern = f'{datetime.now().year}-{datetime.now().month:02d}-{datetime.now().day:02d}'

        # Create the url to request the data from TheGuardian:
        request_url = f'https://content.guardianapis.com/search' \
                      f'?api-key={THEGUARDIAN_API_KEY}' \
                      f'&q={search_string}' \
                      f'&from-date={date_pattern}' \
                      f'&lang=en'

        # Try to get the json from the request or throw an error:
        try:
            results = requests.get(request_url).json()

            # Access the 'response'/'results' in the json:
            json_data = results['response']['results']

            # Loop through each element of the json data:
            for i in range(len(json_data)):
                block = json_data[i]

                # Get the 'webTitle' and 'webUrl':
                title = block['webTitle']
                url = block['webUrl']

                # Yield the article to the caller:
                yield ['', title, url]

        except Exception as get_news_e:
            raise ValueError(f'TheGuardianAPI/get_news exception: {get_news_e}')

    else:
        raise ValueError(f'Empty fields were found in NovaScotiansBotConfig for TheGuardianAPI')
# endregion get_news()

# endregion Methods
