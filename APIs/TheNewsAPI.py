"""
TheNewsAPI

    This script contains the methods used to pull data from https://TheNewsAPI.com/

    API Documentation: https://www.thenewsapi.com/documentation
    An example url to search for news articles:
    api.thenewsapi.com/v1/news/all?api_token={THENEWSAPI_KEY}&search={search_string}&published_on={todays_date}&language=en

"""
import requests
from datetime import datetime
from AccountConfiguration.AccountConfig import THENEWSAPI_KEY

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
    # Clean the search_string as required for this API (special characters (+, -, |, ", *, ()) MUST be URL-encoded)
    search_string = search_string.strip().replace(' ', '%20').replace('"', '%22')

    # Get today's date for the search
    todays_date = f'{datetime.now().year}-{datetime.now().month:02d}-{datetime.now().day:02d}'

    # Create the url to request the data from TheNewsAPI:
    request_url = f'https://api.thenewsapi.com/v1/news/all' \
                  f'?api_token={THENEWSAPI_KEY}' \
                  f'&search={search_string}' \
                  f'&published_on={todays_date}' \
                  f'&language=en'

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