# <u><i>NovaScotiansBot</i></u>
Python 3 code to drive a Nova Scotia news bot reddit account, [NovaScotiansBot](https://www.reddit.com/u/NovaScotiansBot/), which will scan news APIs for Nova Scotia related articles, and then post them to https://www.reddit.com/r/NovaScotians/. 

## Usage:
- Get a https://www.reddit.com account and API set up, and assign the private data to the relevant variables inside ../AccountConfiguration/AccountConfig.py
- Get a https://www.mediastack.com account and API set up, and assign the private data to the relevant variables inside ../AccountConfiguration/AccountConfig.py
- Get a https://www.thenewsapi.com account and API set up, and assign the private data to the relevant variables inside ../AccountConfiguration/AccountConfig.py
- Use <u>Python 3</u> to run <b>NovaScotiansBot.py</b>.
- The script will run on a loop, posting every 15 minutes for any posts not yet posted to reddit, or every 1.5 hours if all posts have been posted to reddit (this prevents excessive news API calls).
- CTRL+C will terminate the script (but you should probably wait until it displays '<b><i>Waiting to run again @ yyyy-MM-DD HH:mm:ss.fff (CTRL+C to QUIT)</i></b>' to avoid the small risk of data-loss when writing to Posts.csv)
- The script identifies if it has posted an article to reddit using Posts.csv, where the 1st column of data = 'Posted'.
- Could cause a problem of reposting if you delete Posts.csv.


## ToDo's:
- Find a way to make sure only english language posts are posted.
- Add some more News APIs.
- Switch from csv files to SQLite or TinyDB.
- Other improvements?
