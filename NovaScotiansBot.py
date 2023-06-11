"""
NovaScotiansBot

    This application contains the processes required to find news articles, and post the articles to Reddit.

    Additionally, this application will cycle a monthly Chat Lounge sticky for the subreddit, if the account
    has mod privileges and sets the following User Variable to True:
        this_bot_is_a_mod_and_will_cycle_a_monthly_chat_lounge

    Source:
        https://github.com/xTkAx/NovaScotiansBot

"""
# region Libraries:
import csv
import os
import shutil
import sys
import time
from datetime import datetime, timedelta
from APIs import RedditAPI, MediaStackAPI, TheNewsAPI, TheGuardianAPI, GNewsAPI

# endregion Libraries

# region Variables:

# region User:

user_defined_search_strings = ['Nova Scotia', 'Scotian']  # This is what you want to edit (each '*' is 1 search).

this_bot_is_a_mod_and_will_cycle_a_monthly_chat_lounge = True  # [True] or [False]?

posts_file = 'NovaScotiansPosts.csv'  # The filename to store all the article data (rows of: ["Posted","title","url"]).

archive_posts_file = False  # [True] will reset the posts_file every day.  [False] will continue appending to post_file.

default_retry_delay = 5400  # Delay before retrying the APIs (lowers API calls which can run out in a month). - 1.5h

repost_retry_delay = 900  # Delay for reddit if there are any more posts left to post from posts_file. - 15m

# endregion User

# region Application:

# Define a string for posts_file records, to denote a record was successfully posted to reddit:
successfully_posted_string = 'Posted'

# Define the file name where the application's persistent date data will be stored (used for day/month changes):
persistent_date_file = 'NovaScotiansBot.dat'

# Define if articles rejected by custom search in the APIs code should display to the screen [True], or not [False]:
display_rejects = False

# Define the application start_time:
start_time = datetime.now()

# Define the day:
current_day = f'{start_time.year}{start_time.month:02d}{start_time.day:02d}'

# endregion Application

# endregion Variables

# region Methods:

# region Files:

# region get_csv_array():
"""
    This method will read a csv file and return an array of records from it.
    
    Parameters:
        filename:       The path to the csv file.
    
    Returns:
        An array, including any successfully retrieved records.

"""


def get_csv_array(filename):
    return_array = []

    if os.path.exists(filename):

        try:  # Open the file:
            with open(filename, newline='') as csv_file:

                # Create a csv reader object:
                csv_reader = csv.reader(csv_file)

                for record in csv_reader:
                    return_array.append(record)

            print(f'{filename} was read.')

        except Exception as get_csv_array_e:
            print(f'get_csv_array() exception: {get_csv_array_e}')

    else:
        print(f'{filename} does not exist.')

    return return_array


# endregion get_csv_array()

# region write_csv():
"""
    This method will write a csv_data object to a csv file.

    Parameters:
        csv_data:       The csv_data to write to a file.
        filename:       The name of the file to write to.
        
    Returns:
        None.

"""


def write_csv(csv_data, filename):
    try:  # Write the file:
        with open(filename, 'w', newline='') as csv_file:

            csv_writer = csv.writer(csv_file)

            for record in csv_data:
                csv_writer.writerow(record)

            print(f'{filename} was written.')

    except Exception as write_csv_e:
        print(f'write_csv() exception: {write_csv_e}')


# endregion write_csv()

# region archive_file():
"""
    This method will move a file to a new name, prefixed with a time stamp, to archive it.

    Parameters:
        filename:       The name of the filename to archive.
        timestamp:      The prefix for the filename.
        
    Returns:
        None.

"""


def archive_file(filename, timestamp):
    seperator = '.'  # eg: 'timestamp.filename'

    # Define the archive file name:
    archive_filename = f'{timestamp}{seperator}{filename}'

    try:  # Archive the filename:
        shutil.move(filename, archive_filename)

        print(f'{filename} archived @ {archive_filename}.')

    except Exception as archive_file_e:
        print(f'archive_file() exception: {archive_file_e}')


# endregion archive_file()

# region delete_file():
"""
    This method will delete a file.  

    Parameters:
        filename:       The filename to delete.

    Returns:
        None.

"""


def delete_file(filename):
    try:  # Delete file:
        if os.path.exists(filename):
            os.remove(filename)

            print(f'{filename} was purged.')

    except Exception as delete_file_e:
        print(f'delete_file() exception: {delete_file_e}')


# endregion delete_file()

# endregion Files

# region Data:

# region get_last_run_date():
"""
    This method will attempt to get the application's last run date from a file.
        
    Parameters:
        filename:       The name of the file holding the application's persistent date.
    
    Returns:
        yyyyMMdd value found in the file, or 0.

"""


def get_last_run_date(filename):
    # Set the return value:
    return_value = 0

    # Get the date record from the persistent_date_file:
    run_date = get_csv_array(filename)

    # If there is one line of data:
    if len(run_date) == 1:
        # Set the return_value with the data:
        return_value = run_date[0][0]

        print(f'Using last run date of {return_value}.')

    else:
        # If the file exists:
        if os.path.exists(filename):
            # Alert the user of unexpected data in the file:
            print(f'{filename} was expected to have 1 row of data, but had {len(last_run_date)}.')

    return return_value


# endregion get_last_run_date()

# region count_col_matches():
"""
    This method will count the number of matches or non-matches for
    a column of data in a csv_array of data.
        
    Parameters:
        csv_array:      The array of csv data.
        match_value:    The search value to match.
        match:          Switch to handle counting matches [True](default) or non-matches [False].
        column:         Column of csv_array data to analyze (default = 0).
    
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


# endregion count_col_matches()

# region add_new_articles_to_post_data():
"""
    This method will identify any new_posts not in posts, then add them to posts, and return the object.  

    Parameters:
        new_posts:          The new posts array to compare and populate missing articles from.
        posts:              The posts array to compare and populate to.

    Returns:
        The updated posts object.

"""


def add_new_articles_to_post_data(new_posts, posts):
    new_posts_count = 0

    for article in new_posts:

        new_title = article[1]  # Assuming Title column is always the 2nd column.

        new_url = article[2]  # Assuming URL column is always the 3rd column.

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


# endregion add_new_articles_to_post_data()

# endregion Data

# region Reddit:

# region post_unposted_to_reddit():
"""
    This method will post any un-posted posts to reddit.

    Parameters:
        posts_array:    The array of post csv data.
        match_value:    The value to search and update the posts object with.
        column:         The column of data to search on (Default = 0).

    Returns:
        The modified posts object.

"""


def post_unposted_to_reddit(posts_array, match_value, column=0):

    print(f'Posting to Reddit:')

    for article in posts_array:

        if article[column].upper() != match_value.upper():

            try:  # Post the article to reddit:
                RedditAPI.post_article_to_reddit(article[1], article[2])  # Assume title & url is the 2nd & 3rd column.

                article[column] = match_value

                print(f'\tPosted: {article[1]} | {article[2]}')

            except Exception as post_unposted_to_reddit_e:
                print(f'\tpost_unposted_to_reddit() exception: {post_unposted_to_reddit_e}')

    return posts_array


# endregion post_unposted_to_reddit()

# region cycle_new_chat_lounge():
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
    print(f'Cycling Reddit Chat Lounge:')

    lounge_date = f"{current_date.strftime('%B')}, {current_date.now().year}"  # eg: "June, 2023".

    lounge_title = f'Chat Lounge For {lounge_date}'  # RedditAPI will prefix this. eg: 'r/SubredditName {lounge_title}'.

    lounge_body = f'#The {lounge_date} Chat Lounge - Chat about *anything** you want!\r\n' \
                  f'*Within reddit rules & with somewhat relaxed sub-rules - Be yourself (but not an ass)!\r\n'

    try:  # Cycle a new Chat Lounge:
        RedditAPI.cycle_to_new_monthly_chat_lounge(lounge_title, lounge_body)

    except Exception as cycle_new_chat_lounge_e:
        print(f'\tcycle_new_chat_lounge() exception: {cycle_new_chat_lounge_e}')


# endregion cycle_new_chat_lounge():

# endregion Reddit

# region News:

# region get_articles_from_apis():
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

            print(f'\t\t{article_count} articles @ MediaStack')

        except Exception as mediastack_e:
            print(f'\t\tMediaStackAPI exception: {mediastack_e}')

        try:  # Get TheNewsAPI articles:
            article_count = 0

            for article in TheNewsAPI.get_news(search_string):
                return_articles.append(article)
                article_count += 1

            print(f'\t\t{article_count} articles @ TheNewsAPI')

        except Exception as thenewsapi_e:
            print(f'\t\tTheNewsAPI exception: {thenewsapi_e}')

        try:  # Get TheGuardianAPI articles:
            article_count = 0

            for article in TheGuardianAPI.get_news(search_string):
                return_articles.append(article)
                article_count += 1

            print(f'\t\t{article_count} articles @ TheGuardianAPI')

        except Exception as theguardianapi_e:
            print(f'\t\tTheGuardianAPI exception: {theguardianapi_e}')

        try:  # Get GNewsAPI articles:
            article_count = 0

            for article in GNewsAPI.get_news(search_string):
                return_articles.append(article)
                article_count += 1

            print(f'\t\t{article_count} articles @ GNewsAPI')

        except Exception as theguardianapi_e:
            print(f'\t\tGNewsAPI exception: {theguardianapi_e}')

        # Add another API here:

    return return_articles


# endregion get_articles_from_apis()

# endregion News

# endregion Methods

# region Application:

# If the user set either of these to True:
if this_bot_is_a_mod_and_will_cycle_a_monthly_chat_lounge or archive_posts_file:

    # Get the last run date from the persistent_date_file:
    last_run_date = get_last_run_date(persistent_date_file)

    # Set the current day:
    current_day = current_day if last_run_date == 0 else last_run_date

else:
    # Attempt to purge the persistent_date_file:
    delete_file(persistent_date_file)

while True:
    # Define the start time for this loop:
    loop_start_time = datetime.now()

    # Define date variables for this loop:
    loop_start_day = f'{loop_start_time.year}{loop_start_time.month:02d}{loop_start_time.day:02d}'
    loop_start_month = f'{loop_start_time.year}{loop_start_time.month:02d}'
    current_month = current_day[:(len(current_day) - 2)]

    # Get an array of data from the posts_file (or empty array if posts_file is empty or non-existent):
    post_data = get_csv_array(posts_file)

    # Identify the number of unposted posts in post_data:
    unposted_count = count_col_matches(post_data, successfully_posted_string, False)

    print(f'{unposted_count} not yet posted.') if unposted_count != 0 else print(f'No unposted data found.')

    # If there is nothing to post:
    if unposted_count == 0:

        # If the loop is in a new day:
        if loop_start_day != current_day:

            # If the posts_file exists, and the user set archive_posts_file = True:
            if os.path.exists(posts_file) and archive_posts_file:

                # Archive the file for the last day:
                archive_file(posts_file, current_day)

                # Reset the post_data in memory:
                post_data = []

            # Set the current day value to this day:
            current_day = loop_start_day

        # If the loop is in a new month and the user set this to True:
        if loop_start_month != current_month and this_bot_is_a_mod_and_will_cycle_a_monthly_chat_lounge:

            # Cycle the chat lounge
            cycle_new_chat_lounge(loop_start_time)

        # Get new articles:
        new_articles = get_articles_from_apis(user_defined_search_strings)

        # Add any new_articles not in post_data to post_data:
        post_data = add_new_articles_to_post_data(new_articles, post_data)

    # Identify how many unposted posts in the posts_data again:
    unposted_count = count_col_matches(post_data, successfully_posted_string, False)

    # If there's now any unposted posts in post_data:
    if unposted_count != 0:
        # Post any unposted posts to reddit:
        post_data = post_unposted_to_reddit(post_data, successfully_posted_string)

        # Write the new CSV file with the updated data:
        write_csv(post_data, posts_file)

    # If the user set either of these to true, write the current_day value to the persistent_date_file:
    if this_bot_is_a_mod_and_will_cycle_a_monthly_chat_lounge or archive_posts_file:
        write_csv([[current_day]], persistent_date_file)

    # Initialize the retry_delay:
    retry_delay = default_retry_delay if count_col_matches(post_data, successfully_posted_string, False) == 0 \
        else repost_retry_delay

    # Display the wait and quit message:
    print(f'Waiting to run again in {retry_delay} seconds, @ {datetime.now() + timedelta(seconds=retry_delay)}' +
          f'\r\n(CTRL+C to QUIT)')

    # Pause and wait for retry_delay seconds before running the loop again:
    try:
        time.sleep(retry_delay)

    except:
        print(f'\nApplication run time: {datetime.now() - start_time}\r\nSuccessfully terminated.')
        sys.exit()

# endregion Application
