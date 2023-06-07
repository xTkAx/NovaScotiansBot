# <u><i>NovaScotiansBot</i></u>
Python 3 code to drive a Nova Scotia news bot reddit account, [NovaScotiansBot](https://www.reddit.com/u/NovaScotiansBot/), which will scan news APIs for Nova Scotia related articles, and then post them to https://www.reddit.com/r/NovaScotians/. 

## Usage:
- Set up an account & API access for the following services, and assign the private data to the relevant variables inside <b>../AccountConfiguration/AccountConfig.py</b>:
  -  https://www.reddit.com (Reddit API)
  -  https://www.mediastack.com (News API) 
  -  https://www.thenewsapi.com (News API)
- Use <B>Python 3</B> to run <b>NovaScotiansBot.py</b>.
- The script will run on a loop:
  - Every 15 minutes if there are any posts in Posts.csv yet to be posted to reddit.
  - Every 1.5 hours if all posts have been posted to reddit (prevents excessive news API calls).
- CTRL+C will terminate the script (It's best to wait until it displays '<b><i>Waiting to run again @ yyyy-MM-DD HH:mm:ss.fff (CTRL+C to QUIT)</i></b>' to avoid a <i>small</i> risk of data-loss when writing to Posts.csv)
- The script identifies if it has posted an article to reddit using Posts.csv, where the 1st column of data = '<b>Posted</b>'.
- When a new day is detected, the script will move Posts.csv to Posts.csv<i>yyyyMMdd</i> and begin a new Posts.csv
## Issues:
- Could cause a problem of reposting if you delete Posts.csv.
- Can be a bit limited with free api accounts.
- Someone might forget to delete backup <i>Posts.csvyyyyMMdd</i> files and run out of space :(.


## ToDo's:
- Find a way to make sure only english language posts are posted.
- Add more News APIs.
