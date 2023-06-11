"""
MediaStackAPI

    This file contains the methods used to pull data from https://MediaStack.com/
    -Free account allows 500 requests per month.
    -Free account only allows http access (no https).
    -An example url to search for news articles:
    api.mediastack.com/v1/news?access_key={MEDIASTACK_API_KEY}&keywords={search_string}&date={date}&languages=en

    Documentation:
        https://mediastack.com/documentation

    Source:
        https://github.com/xTkAx/NovaScotiansBot

"""
# region Libraries:
import re
import requests
from datetime import datetime
from NovaScotiansBotConfig import MEDIASTACK_API_KEY

# endregion Libraries:

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
    if MEDIASTACK_API_KEY == '':
        return False
    else:
        return True


# endregion confirm_user_config()

# region get_news()
"""
get_news()
    This method will generate the query to get the news from MediaStack.com, and yield each article back to the caller.
    
    Parameters:
        search_string:  The string to do a news search for.
        show_rejects:   Will show any custom search rejects.
            
    Yields:
        Articles of data in the format:
            ['', title, url]
    
    Throws:
        Error.
            
"""


def get_news(search_string, show_rejected=False):
    # If the user filled all fields in NovaScotiansBotConfig:
    if confirm_user_config():

        # Clean the search_string as required for this API:
        search_string = f'{search_string.strip().replace(" ", "%20")}'

        # Get today's date for the search
        date_pattern = f'{datetime.now().year}-{datetime.now().month:02d}-{datetime.now().day:02d}'

        # Create the url to request the data from MediaStackAPI:
        request_url = f'http://api.mediastack.com/v1/news' \
                      f'?access_key={MEDIASTACK_API_KEY}' \
                      f'&keywords={search_string}' \
                      f'&date={date_pattern}' \
                      f'&languages=en'

        # Try to get the json from the request or throw an error:
        try:
            results = requests.get(request_url).json()

            # Access the 'data' in the json:
            json_data = results['data']

            # Loop through each element of the json data:
            for i in range(len(json_data)):
                block = json_data[i]

                # Get the 'title' and 'url':
                title = block['title']
                url = block['url']

                # Get the description too:
                description = block['description']

                # Redefine search, title, url, desc, to remove all non-alphanumerics and make string uppercase for
                # testing, because this API searches "multiple terms" as 'multiple OR terms' and gets many false hits:
                test_search_regex = re.sub(r'\W+', '', search_string.replace('%20', '').upper())
                test_title = re.sub(r'\W+', '', title.upper())
                test_url = re.sub(r'\W+', '', url.upper())
                test_desc = re.sub(r'\W+', '', description.upper())

                # Check all tests and skip any entries where test_search_regex is not in test_title/url/desc:
                if not re.search(test_search_regex, test_title):
                    if not re.search(test_search_regex, test_url):
                        if not re.search(test_search_regex, test_desc):
                            if show_rejected:
                                print(f'\t\tMediaStackAPI custom reject: {title} | {url}')
                            continue

                # Yield the article to the caller:
                yield ['', title, url]

        except Exception as get_news_e:
            raise ValueError(f'MediaStackAPI/get_news exception: {get_news_e}')

    else:
        raise ValueError(f'Empty fields were found in NovaScotiansBotConfig for MediaStackAPI')

# endregion get_news()

# endregion Methods
