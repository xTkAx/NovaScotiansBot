# NovaScotiansBot
A Nova Scotia news bot which will scan News API's and then post links to the news articles to https://www.reddit.com/r/NovaScotians/  

## Usage:
- Get a Reddit.com API set up with an account and place the private data in the variables inside ../AccountConfiguration/AccountConfig.py
- Get a MediaStack.com API set up with an account and place the private data in the variables inside ../AccountConfiguration/AccountConfig.py
- Run NovaScotiansBot.py using Python 3.
- The script will run on a loop, posting every 15 minutes for any posts not yet posted to reddit, or every 1.5 hours if all posts have been posted to reddit.
- The script identifies if it has posted using Posts.csv, where the 1st column of data = 'Posted'.
- Could cause a problem of reposting if you delete Posts.csv.


## ToDo's:
- Find a way to make sure only english language posts are posted.
- Add some more News API's.
- Switch from csv files to SQLite or TinyDB.
- Other improvements?
