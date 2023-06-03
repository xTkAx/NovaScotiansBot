"""
MediaStackNewsAPI ( https://mediastack.com/ )

    This script contains the methods used to pull data from https://mediastack.com/
    -Free account allows 500 requests per month.
    -Free account only allows http access.

    An example url to search for Nova Scotia news articles would be:
    http://api.mediastack.com/v1/news?access_key={MEDIASTACK_API_KEY}&languages=en&keywords=Nova+Scotia&date={url_date}

"""
import requests
from datetime import datetime
from AccountConfiguration.AccountConfig import MEDIASTACK_API_KEY

# region get_news()
"""
get_news()
    This method will generate the query to get the news from MediaStack.com
    It will return an array of return_data eg:
        [
            ['', title1, url1],
            ['', title2, url2],
            ['', titleN, urlN]
        ]
"""


def get_news():
    # Get today's date for the search
    url_date = f'{datetime.now().year}-{datetime.now().month:02d}-{datetime.now().day:02d}'

    # Request the data from MediaStackNewsAPI:
    request_url = f'http://api.mediastack.com/v1/news?access_key={MEDIASTACK_API_KEY}' \
                  f'&languages=en&keywords=Nova+Scotia&date={url_date}'

    # Try to get the json from the request:
    try:
        results = requests.get(request_url).json()
    except Exception as e:
        raise ValueError(e)

    # Access the 'data' in the json:
    json_data = results['data']

    # Create a data object to return to caller:
    return_data = []

    # Loop through each element of the json data:
    for i in range(len(json_data)):
        block = json_data[i]

        # Get the 'title' and 'url':
        title = block['title']
        url = block['url']

        # Append it to the return_data:
        return_data.append(['', title, url])

    return return_data
# endregion get_news()
