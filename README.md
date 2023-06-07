# <u><i>NovaScotiansBot</i></u>
Python 3 code to drive a Nova Scotia news bot reddit account, [NovaScotiansBot](https://www.reddit.com/u/NovaScotiansBot/), which will scan news APIs for Nova Scotia related articles, and then post them to https://www.reddit.com/r/NovaScotians/. 

Can be modified to become your own subreddit news bot!

## How To Use:
- Set up an account for your bot & get API keys for the following services:
  -  https://www.reddit.com (Reddit API) +
     - Find a subreddit to use the bot in (work with a mod, or make a new one).
  -  https://www.mediastack.com (News API) 
  -  https://www.thenewsapi.com (News API)
- Assign the private data to the relevant variables inside the file: <b>./AccountConfiguration/AccountConfig.py</b>
- Look in the file <b>NovaScotiansBot.py</b> for the following code:
  - <code>search_strings = ['Nova Scotia', 'Scotians', 'Scotian']</code>
  - Replace <b>'Nova Scotia', 'Scotians', 'Scotian'</b> with what keywords you want to get news for.
- Use <B>Python 3</B> to run <b>NovaScotiansBot.py</b>:
  - <code>python3 NovaScotiansBot.py </code>
  - The script will run on a loop:
    - Every 15 minutes if there are any posts in Posts.csv yet to be posted to reddit.
    - Every 1.5 hours if all posts have been posted to reddit (prevents excessive news API calls).
  - CTRL+C will terminate the script.
    - To avoid the small risk of data-loss when writing to Posts.csv, only press CTRL+C when you see: '<b><i>Waiting to run again @ yyyy-MM-DD HH:mm:ss.fff (CTRL+C to QUIT)</i></b>'.
  - The script identifies if it has posted an article to reddit using Posts.csv, where the 1st column of data = '<b>Posted</b>'.
  - When a new day is detected, the script will move Posts.csv to Posts.csv<i>yyyyMMdd</i> and begin a new Posts.csv

## Issues:
- You might have to install some libraries.
- Could cause a problem of reposting if you delete Posts.csv.
- Might be a bit limited with free API accounts.
- You might forget to delete backup <i>Posts.csvyyyyMMdd</i> files, and they could build up to consume all your free space :(.


## ToDo's:
- Find a way to make sure only english language posts are posted.
- Add more News APIs.
