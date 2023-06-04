"""
NovaScotiansBot

    This script contains the processes required to post news articles to https://www.reddit.com/r/NovaScotians

"""
import csv
import os
import sys
import time
from datetime import datetime, timedelta
from APIs import MediaStackNewsAPI, RedditAPI

# Define the default delay in seconds before a retry:
default_retry = 5400  # Every 1.5 hours

# Define the Posts csv file:
posts_file = 'Posts.csv'

# Define the search string:
search_string = 'Nova Scotia'

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
    if non_posted == 0:
        # Try to get news from MediaStackNewsAPI:
        print('Gathering data from MediaStackNewsAPI.')
        try:
            mediastack_news = MediaStackNewsAPI.get_news(search_string)
            print(f'{len(mediastack_news)} news items gathered.')
        except Exception as e:
            print(f'Exiting program due to MediaStackNewsAPI error:\r\n{e}')
            sys.exit()  # Exit on error
        new_posts = 0
        # Loop through mediastack_news and check if entry is in post_data
        for mediastack_entry in mediastack_news:
            mediastack_title = mediastack_entry[1]  # assuming Title column is always the 2nd column
            mediastack_url = mediastack_entry[2]  # assuming URL column is always the 3rd column
            entry_found = False
            for post_entry in post_data:
                post_title = post_entry[1]
                post_url = post_entry[2]
                if mediastack_url == post_url or mediastack_title == post_title:
                    entry_found = True
                    break
            # If entry not found in post_data, append the mediastack_entry to post_data
            if not entry_found:
                post_data.append(mediastack_entry)
                non_posted += 1  # subtract one from non_posted to keep track and identify which delay to use later.
        print(f'{new_posts} new posts were retrieved from MediaStackNewsAPI.')

    # Loop through non-posted post_data and create a reddit post of data:
    for entry in post_data:
        if entry[0] != 'Posted':
            try:
                RedditAPI.post_article(entry[1], entry[2])  # assuming TITLE & URL column is the 2nd & 3rd column
                entry[0] = 'Posted'
                print(f'Posted:\r\n\t{entry[1]}\r\n\t{entry[2]}')
                non_posted -= 1
            except Exception as e:
                print(f'Error Posting:\r\n\t{entry[1]}\r\n\t{entry[2]}\r\n\t[ {e} ]')

    # Write the new CSV file with the updated data:
    with open(posts_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in post_data:
            writer.writerow(row)
        print(f'Wrote {posts_file}.')

    # Set the retry delay to 15 minutes (reddit repost limit)
    retry_delay = 900

    # But if there's no un-posted entries in posts_file, set retry_delay to default_retry to lower news API calls.
    if non_posted <= 0:
        retry_delay = default_retry

    # Pause and wait for a re-run.
    print(f'Waiting to run again @ {datetime.now() + timedelta(seconds=retry_delay)} (CTRL+C to QUIT)')
    try:
        time.sleep(retry_delay)
    except:
        print(f"\nTerminated by user")
        sys.exit()
