"""
MediaStackAPI

    This script contains the methods used to pull data from https://mediastack.com/
    -Free account allows 500 requests per month.
    -Free account only allows http access.

    An example url to search for news articles:
    api.mediastack.com/v1/news?access_key={MEDIASTACK_API_KEY}&keywords={search_string}&date={todays_date}&languages=en

"""
import requests
from datetime import datetime
from AccountConfiguration.AccountConfig import MEDIASTACK_API_KEY

# region get_news()
"""
get_news()
    This method will generate the query to get the news from MediaStack.com, and return an array of data to the
    caller (or will throw an error).
    
    Parameters:
        search_string: the string to do a news search for
        
    Returns:
        (good) An array of return_data:
            eg:
            [['', title1, url1],['', title2, url2],['', titleN, urlN],..]
            
        (bad) it will throw an error
    
"""


def get_news(search_string):
    # Clean the search_string as required for this API:
    search_string = search_string.strip().replace(' ', '+')

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

        # Yield the article to the caller:
        yield ['', title, url]
# endregion get_news()