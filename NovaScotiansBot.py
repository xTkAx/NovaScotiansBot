"""
NovaScotiansBot

    This script contains the processes required to post news articles to https://www.reddit.com/r/NovaScotians

"""
import csv
import os
import sys
from APIs import MediaStackNewsAPI, RedditAPI

# Define the Posts csv file:
posts_file = 'Posts.csv'

# Initialize an empty list to store data from posts_file
post_data = []

# Check if posts_file exists:
if os.path.exists(posts_file):
    all_posts = 0
    # Open the CSV file
    print(f'Reading {posts_file}')
    with open(posts_file, newline='') as csvfile:
        # Create a CSV reader object
        reader = csv.reader(csvfile)
        # Loop through each row in the file and append it to the data list
        for row in reader:
            post_data.append(row)
            all_posts += 1
    print(f'{all_posts} posts were found in {posts_file}.')
else:
    print(f'{posts_file} does not exist')


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
        mediastack_news = MediaStackNewsAPI.get_news()
    except Exception as e:
        print(e)
        sys.exit()  # Exit on error
    new_posts = 0
    # Loop through mediastack_news and check if URL is in post_data
    for mediastack_entry in mediastack_news:
        mediastack_title = mediastack_entry[1] # assuming Title column is always the 3rd column
        mediastack_url = mediastack_entry[2]  # assuming URL column is always the 3rd column
        entry_found = False
        for post_entry in post_data:
            post_title = post_entry[1]
            post_url = post_entry[2]
            if mediastack_url == post_url or mediastack_title == post_title:
                entry_found = True
                break
        # If URL not found in post_data, append the mediastack_entry to post_data
        if not entry_found:
            post_data.append(mediastack_entry)
            new_posts += 1
    print(f'{new_posts} new posts were retrieved from MediaStackNewsAPI.')

# Loop through non-posted post_data and create a reddit post of data:
for entry in post_data:
    if entry[0] != 'Posted':
        try:
            RedditAPI.post_article(entry[1], entry[2])  # assuming TITLE & URL column is always the 2nd & 3rd column
            entry[0] = 'Posted'
            print(f'Posted:\r\n\t{entry[1]}\r\n\t{entry[2]}')
        except Exception as e:
            print(e)

# Write the new CSV file with the updated data:
with open(posts_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for row in post_data:
        writer.writerow(row)
    print(f'Wrote {posts_file}')
