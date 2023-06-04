# NovaScotiansBot
A news bot for https://www.reddit.com/r/NovaScotians/

# Usage
-Get a Reddit.com API set up with an account and private data placed in ../AccountConfiguration/AccountConfig.py

-Get a MediaStack.com API set up and private data placed in ../AccountConfiguration/AccountConfig.py

-Run NovaScotiansBot.py using Python 3.

-Scritp will run on a loop, posting every 15 minutes for any posts not yet posted to reddit, or every 1.5 hours if all posts have been posted to reddit.

-The script identifies if it has posted using Posts.csv, where the 1st column of data = 'Posted'.

-Could cause a problem of reposting if you delete Posts.csv.
