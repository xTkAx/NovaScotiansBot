"""
MediaStackAPI

    This script contains the methods used to pull data from https://mediastack.com/
    -Free account allows 500 requests per month.
    -Free account only allows http access (no https).

    API Documentation: https://mediastack.com/documentation
    An example url to search for news articles:
    api.mediastack.com/v1/news?access_key={MEDIASTACK_API_KEY}&keywords={search_string}&date={todays_date}&languages=en

"""
import re

import requests
from datetime import datetime
from AccountConfiguration.AccountConfig import MEDIASTACK_API_KEY

# region get_news()
"""
get_news()
    This method will generate the query to get the news from MediaStack.com, and yield each article back to the caller
     (or will throw an error).
    
    Parameters:
        search_string: the string to do a news search for
    
    Throws:
        Error
            
    Yields:
        Articles of data in the format:
            ['', title, url]
            
"""


def get_news(search_string):
    # Clean the search_string as required for this API:
    search_string = f'{search_string.strip().replace(" ", "%20")}'

    # Get today's date for the search
    todays_date = f'{datetime.now().year}-{datetime.now().month:02d}-{datetime.now().day:02d}'

    # Create the url to request the data from MediaStackAPI:
    request_url = f'http://api.mediastack.com/v1/news' \
                  f'?access_key={MEDIASTACK_API_KEY}' \
                  f'&keywords={search_string}' \
                  f'&date={todays_date}' \
                  f'&languages=en'

    # Try to get the json from the request or throw an error:
    try:
        results = requests.get(request_url).json()
    except Exception as e:
        raise ValueError(e)

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

        # For this API we need to check titles urls and descriptions for the search_string
        # because it's a bad API that will search "multiple terms" as 'multiple OR terms'.
        # It's hacky and messy, but works:
        test_search_regex = search_string.replace('%20', '').upper()
        test_title = title.strip().replace('-', '').replace('.', '').replace(' ', '').replace(',', '').upper()
        test_url = url.strip().replace('-', '').replace('.', '').replace(' ', '').replace(',', '').\
            replace('/', '').replace(':', '').replace('(', '').replace(')', '').replace('\'', '').upper()
        test_desc = description.strip().replace('-', '').replace('.', '').replace(' ', '').replace(',', '').\
            replace('/', '').replace(':', '').replace('(', '').replace(')', '').replace('\'', '').upper()
        # Check all tests and skip any entries where the title, url or description don't match the search_string:
        if not re.search(test_search_regex, test_title):
            if not re.search(test_search_regex, test_url):
                if not re.search(test_search_regex, test_desc):
                    continue

        # Yield the article to the caller:
        yield ['', title, url]
# endregion get_news()
