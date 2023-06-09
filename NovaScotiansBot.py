"""
NovaScotiansBot

    This script contains the processes required to post news articles to https://www.reddit.com/r/NovaScotians

    https://github.com/xTkAx/NovaScotiansBot

"""
# region Libraries
import csv
import os
import shutil
import sys
import time
from datetime import datetime, timedelta
from APIs import RedditAPI, MediaStackAPI, TheNewsAPI

# endregion Libraries


# region User-Defined Variables:

user_defined_search_strings = ['Nova Scotia', 'Scotian']  # Yes! this is what you want to edit!

this_bot_is_a_mod_and_will_cycle_a_monthly_chat_lounge = True  # True or False?

archive_posts_file = True  # True will reset the posts_file every day.  False will keep building up 1 post_file.

posts_file = 'Posts.csv'  # The filename where all the daily article data is stored.

default_retry = 5400  # 1.5 hour delay before retrying the APIs (lowers API calls which can run out in a month).

reddit_retry = 900  # 15 minute reddit delay if there are still more posts left to post from posts_file.

# endregion User-Defined Variables


# region Script Variables:

# Define a string for posts_file records to record a successful reddit post:
successful_post_string = 'Posted'

# Define the file name where the script's persistent date data will be stored (to know where the date last left off).
persistent_date_file = 'NovaScotiansBot.dat'

# This will display any rejected posts from APIs with a custom article search.
display_rejects = False

# Get the script start_time:
start_time = datetime.now()

# Define time variables:
current_day = f'{start_time.year}{start_time.month:02d}{start_time.day:02d}'
current_month = f'{start_time.year}{start_time.month:02d}'

# endregion Script Variables


# region Methods:

# region get_csv_array(file):
"""
    This method will read a csv file and return an array of records from it.
    
    Parameters:
        file:           The path to the csv file.
    
    Returns:
        An array, including any successfully retrieved records.

"""


def get_csv_array(file):
    return_array = []

    if os.path.exists(file):

        try:  # Open the file:
            with open(file, newline='') as csv_file:

                # Create a csv reader object:
                csv_reader = csv.reader(csv_file)

                for record in csv_reader:
                    return_array.append(record)

            print(f'{file} was read.')

        except Exception as get_csv_array_e:
            print(f'get_csv_array() exception: {get_csv_array_e}')

    else:
        print(f'{file} does not exist.')

    return return_array


# endregion get_csv_array(file)

# region write_csv(csv_data, file):
"""
    This method will write a csv_data object to a csv file.

    Parameters:
        csv_data:       The csv_data to write to a file.
        file:           The name of the file to write to.
        
    Returns:
        None.

"""


def write_csv(csv_data, file):
    try:  # Write the file:
        with open(file, 'w', newline='') as csv_file:

            csv_writer = csv.writer(csv_file)

            for record in csv_data:
                csv_writer.writerow(record)

            print(f'{file} was written.')

    except Exception as write_csv_e:
        print(f'write_csv() exception: {write_csv_e}')


# endregion write_csv(csv_data, file)

# region count_col_matches(csv_array, match_value, match=True, column=0):
"""
    This method will count the number of matches or non-matches for
    a column of data in a csv_array of data.
        
    Parameters:
        csv_array:      The array of csv data.
        match_value:    The search value to match.
        match:          Switch to handle counting matches [True](default) or non-matches [False]
        column:         Column of csv_array data to analyze (default = 0)
    
    Returns:
        The number of matches or non-matches based on the parameters.

"""


def count_col_matches(csv_array, match_value, match=True, column=0):
    counter = 0

    for record in csv_array:

        # If matching and value matches, or if not matching and value doesn't match:
        if (match and record[column].upper() == match_value.upper()) or \
                (not match and record[column].upper() != match_value.upper()):
            counter += 1

    return counter


# endregion count_col_matches(csv_array, match_value, match=True, column=0)

# region archive_file(filename, timestamp):
"""
    This method will move a fle to a new name, prefixed with a time stamp, to archive it.

    Parameters:
        filename:       The name of the filename to archive.
        timestamp:      The prefix for the filename.
        
    Returns:
        None

"""


def archive_file(filename, timestamp):
    seperator = '.'  # eg: timestamp.filename

    # Define the archive file name:
    archive_filename = f'{timestamp}{seperator}{filename}'

    try:  # Archive (move) the filename:
        shutil.move(filename, archive_filename)

        print(f'{filename} archived@ {archive_filename}.')

    except Exception as archive_e:
        print(f'archive_file() exception: {archive_e}')


# endregion archive_file(filename, timestamp)

# region post_unposted_to_reddit(posts, match_value, column=0):
"""
    This method will post any unposted posts to reddit.

    Parameters:
        posts:          The array of posts.
        match_value:    The value to search and update the posts object with.
        column:         The column of data to search on. (Default = 0)

    Returns:
        The modified posts object.

"""


def post_unposted_to_reddit(posts, match_value, column=0):
    for article in posts:

        if article[column].upper() != match_value.upper():

            try:  # Post it to reddit:
                RedditAPI.post_article(article[1], article[2])  # assuming TITLE & URL column is the 2nd & 3rd column

                article[column] = match_value

                print(f'Posted:\r\n\t{article[1]}\r\n\t{article[2]}')

            except Exception as post_unposted_e:
                print(f'post_unposted_to_reddit() exception: {post_unposted_e}')

    return posts


# endregion post_unposted_to_reddit(posts, match_value, column=0)

# region cycle_new_chat_lounge(current_date):
"""
    This method will cycle the old Chat Lounge of a subreddit and create a new one.
    
    Requires:
        You must have moderator privileges in the subreddit you're using.
    
    Parameters:
        current_date:   A datetime object to get date data.
        
    Returns:
        None.

"""


def cycle_new_chat_lounge(current_date):
    lounge_date = f"{current_date.strftime('%B')}, {current_date.now().year}"  # eg: "June, 2023"

    lounge_title = f'Chat Lounge For {lounge_date}'  # RedditAPI will prefix this. eg: 'r/SubredditName {lounge_title}'

    lounge_body = f'#The {lounge_date} Chat Lounge - Chat about *anything** you want!\r\n' \
                  f'*Within reddit rules & with somewhat relaxed sub-rules - Be yourself (but not an ass)!\r\n'

    try:  # Cycle to a new lounge:
        RedditAPI.create_new_monthly_lounge(lounge_title, lounge_body)

    except Exception as lounge_fail:
        print(f'cycle_new_chat_lounge() exception: {lounge_fail}')


# endregion cycle_new_chat_lounge(current_date):

# region get_articles_from_apis(search_strings):
"""
    This method will get news articles from all APIs.  
    
    This is where you would add more API calls.

    Parameters:
        search_strings:     An array of search strings to search news APIs for.

    Returns:
        An array, including any successfully retrieved news article records.

"""


def get_articles_from_apis(search_strings):
    return_articles = []

    print(f'Searching APIs:')

    for search_string in search_strings:

        print(f'\t"{search_string}":')

        try:  # Get MediaStack articles:
            article_count = 0

            for article in MediaStackAPI.get_news(search_string, display_rejects):
                return_articles.append(article)
                article_count += 1

            print(f'\t\t{article_count} articles@ MediaStack')

        except Exception as mediastack_e:
            print(f'\t\tMediaStackAPI exception: {mediastack_e}')

        try:  # Get TheNewsAPI articles:
            article_count = 0

            for article in TheNewsAPI.get_news(search_string):
                return_articles.append(article)
                article_count += 1

            print(f'\t\t{article_count} articles@ TheNewsAPI')

        except Exception as thenewsapi_e:
            print(f'\t\tTheNewsAPI exception: {thenewsapi_e}')

    return return_articles


# endregion get_articles_from_apis(search_strings)

# region add_new_articles_to_post_data(posts, new_posts):
"""
    This method will identify any new_posts not in posts, then add them to posts, and return the object.  

    Parameters:
        posts:              The posts array to compare and populate to.
        new_posts:          The new posts array to compare and populate missing articles from.

    Returns:
        The updated posts object.

"""


def add_new_articles_to_post_data(posts, new_posts):
    new_posts_count = 0

    for article in new_posts:

        new_title = article[1]  # assuming Title column is always the 2nd column

        new_url = article[2]  # assuming URL column is always the 3rd column

        entry_found = False

        for post_entry in posts:

            post_title = post_entry[1]

            post_url = post_entry[2]

            if new_url.upper() == post_url.upper() or new_title.upper() == post_title.upper():

                entry_found = True

                break

        # If entry not found in posts:
        if not entry_found:

            posts.append(article)

            new_posts_count += 1

    print(f'{new_posts_count} new posts were added.')

    return posts

# endregion add_new_articles_to_post_data(posts, new_posts)

# endregion Methods


# region Main Program:

# If the user set either of these to true, write the program dates to the persistent_date_file:
if this_bot_is_a_mod_and_will_cycle_a_monthly_chat_lounge or archive_posts_file:
    # Get data from the persistent_date_file holding any last_run_dates:
    last_run_dates = get_csv_array(persistent_date_file)

    # If there is one line of data:
    if len(last_run_dates) == 1:
        # Set the times to the new data:
        current_day = last_run_dates[0][0]
        current_month = last_run_dates[0][1]

    else:
        if os.path.exists(persistent_date_file):
            print(f'{persistent_date_file} was expected to have 1 row of data, but had {len(last_run_dates)}.')

# Otherwise purge the persistent_date_file
else:
    if os.path.exists(persistent_date_file):
        os.remove(persistent_date_file)
        print(f'{persistent_date_file} was purged.')

while True:
    # Get the time this loop started:
    loop_start_time = datetime.now()

    # Define time vars for this loop:
    loop_start_day = f'{loop_start_time.year}{loop_start_time.month:02d}{loop_start_time.day:02d}'
    loop_start_month = f'{loop_start_time.year}{loop_start_time.month:02d}'

    # Get an array of data from the posts_file (or empty array if empty/non-existent):
    post_data = get_csv_array(posts_file)

    # Identify the number of unposted_count posts in post_data:
    unposted_count = count_col_matches(post_data, successful_post_string, False)
    print(f'{unposted_count} not yet posted.')

    # If there is nothing to post:
    if unposted_count == 0:

        # If the loop is in a new day:
        if loop_start_day != current_day:

            # If the posts_file exists, and the user set archive_posts_file = True:
            if os.path.exists(posts_file) and archive_posts_file:
                archive_file(posts_file, current_day)
                # Reset post_data:
                post_data = []

            current_day = loop_start_day

        # If the loop is in a new month:
        if loop_start_month != current_month:

            # If this the user set this to true, cycle the chat lounge:
            if this_bot_is_a_mod_and_will_cycle_a_monthly_chat_lounge:
                cycle_new_chat_lounge(loop_start_time)

            current_month = loop_start_month

        # Get new_articles:
        new_articles = get_articles_from_apis(user_defined_search_strings)

        # Add any new_articles not in post_data to post_data:
        post_data = add_new_articles_to_post_data(post_data, new_articles)

    # Try to post the unposted posts to reddit:
    post_data = post_unposted_to_reddit(post_data, successful_post_string)

    # Write the new CSV file with the updated data:
    write_csv(post_data, posts_file)

    # If the user set either of these to true, write the program dates to the persistent_date_file:
    if this_bot_is_a_mod_and_will_cycle_a_monthly_chat_lounge or archive_posts_file:
        write_csv([[current_day, current_month]], persistent_date_file)

    # Initialize the retry_delay:
    retry_delay = default_retry if count_col_matches(post_data, successful_post_string, False) == 0 else reddit_retry

    # Print the wait & quit message:
    print(f'Waiting to run again in {retry_delay} seconds, @ {datetime.now() + timedelta(seconds=retry_delay)} ' +
          f'(CTRL+C to QUIT)')

    # Pause and wait to re-run:
    try:
        time.sleep(retry_delay)

    except:
        print(f'\nProgram run time: {datetime.now() - start_time}\r\nSuccessfully terminated by user.')
        sys.exit()

# endregion Main Program
