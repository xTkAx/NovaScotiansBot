"""
NovaScotiansBot

    This script contains the processes required to post news articles to https://www.reddit.com/r/NovaScotians

"""
import csv
import os
import sys
import time
from datetime import datetime, timedelta
from APIs import RedditAPI, MediaStackAPI, TheNewsAPI

# Define the default delay in seconds before a retry:
default_retry = 5400  # Every 1.5 hours

# Define the reddit replst delay in seconds before a retry:
reddit_retry = 900  # Every 15 minutes

# Define the Posts csv file:
posts_file = 'Posts.csv'

# Define the search strings:
search_strings = ['Nova Scotia', 'Scotians']

# The main program loop (on a timer (see the end))
while True:
    # Initialize an empty list to store data from posts_file
    post_data = []

    # Check if posts_file exists:
    if os.path.exists(posts_file):
        # Open the CSV file
        print(f'Reading {posts_file}')
        with open(posts_file, newline='') as csvfile:
            # Create a CSV reader object
            reader = csv.reader(csvfile)
            # Loop through each row in the file and append it to the data list
            for row in reader:
                post_data.append(row)
        print(f'{len(post_data)} posts were found in {posts_file}.')
    else:
        print(f'{posts_file} does not exist.')

    # Loop through post_data to get the non-posted post_data count:
    non_posted = 0
    for entry in post_data:
        if entry[0] != 'Posted':
            non_posted += 1
    print(f'{non_posted} not posted.')

    # If there is nothing to post:
    if non_posted != 0:
        # Get news from APIs:
        print('Gathering articles from APIs:')
        new_articles = []

        # Iterate through all the search strings:
        for search_string in search_strings:
            print(f'\t"{search_string}":')
            
            # Try get MediaStack articles:
            try:
                article_count = 0
                for article in MediaStackAPI.get_news(search_string):
                    new_articles.append(article)
                    article_count += 1
                print(f'\t\t{article_count} articles found on MediaStack.')
            except Exception as e:
                print(f'\t\tProblem with MediaStackAPI:\r\n\t\t[ {e} ]')

            # Try get TheNewsAPI articles:
            try:
                article_count = 0
                for article in TheNewsAPI.get_news(search_string):
                    new_articles.append(article)
                    article_count += 1
                print(f'\t\t{article_count} articles found on TheNewsAPI.')
            except Exception as e:
                print(f'\t\tProblem with TheNewsAPI:\r\n\t\t[ {e} ]')

        # Loop through new_articles and check if article is in post_data
        new_posts = 0
        for new_article in new_articles:
            new_title = new_article[1]  # assuming Title column is always the 2nd column
            new_url = new_article[2]  # assuming URL column is always the 3rd column
            entry_found = False
            for post_entry in post_data:
                post_title = post_entry[1]
                post_url = post_entry[2]
                if new_url == post_url or new_title == post_title:
                    entry_found = True
                    break
            # If entry not found in post_data, append the new_entry to post_data
            if not entry_found:
                post_data.append(new_article)
                new_posts += 1
        print(f'{new_posts} new posts were retrieved from all APIs.')

    # Loop through non-posted post_data and create a reddit post of data:
    for entry in post_data:
        if entry[0] != 'Posted':
            try:
                RedditAPI.post_article(entry[1], entry[2])  # assuming TITLE & URL column is the 2nd & 3rd column
                entry[0] = 'Posted'
                print(f'Posted:\r\n\t{entry[1]}\r\n\t{entry[2]}')
            except Exception as e:
                print(f'Error Posting:\r\n\t{entry[1]}\r\n\t{entry[2]}\r\n\t[ {e} ]')

    # Write the new CSV file with the updated data:
    with open(posts_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in post_data:
            writer.writerow(row)
        print(f'Wrote {posts_file}.')

    # Loop through post_data again to get the non-posted post_data count:
    non_posted = 0
    for entry in post_data:
        if entry[0] != 'Posted':
            non_posted += 1

    # Initialize the retry delay
    retry_delay = 0

    # Determine when to run again:
    # a) If there's no un-posted entries in posts_file, set retry_delay to default_retry to lower news API calls.
    if non_posted == 0:
        retry_delay = default_retry
    # b) Otherwise set retry_delay to reddit_retry to post sooner.
    else:
        retry_delay = reddit_retry
    run_again_at = datetime.now() + timedelta(seconds=retry_delay)

    # Pause and wait for a re-run.
    print(f'Waiting to run again in {retry_delay} seconds, @ {run_again_at} (CTRL+C to QUIT)')
    try:
        time.sleep(retry_delay)
    except:
        print(f"\nTerminated by user")
        sys.exit()
