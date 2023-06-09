# <u><i>NovaScotiansBot</i></u>
Python 3 code to drive a Nova Scotia news bot reddit account, [NovaScotiansBot](https://www.reddit.com/u/NovaScotiansBot/), which will scan news APIs for Nova Scotia related articles, and then post them to https://www.reddit.com/r/NovaScotians/. 

Can be modified to become your own subreddit news bot!

## How To Use:
- Set up an account for your bot & get API keys for the following services:
  -  https://www.reddit.com (Reddit API) +
     - Find a subreddit to use the bot in (work with a mod, or make a new one), and make it an approved user (or mod user if you want to use Chat Lounge.
  -  https://www.mediastack.com (News API) 
  -  https://www.thenewsapi.com (News API)
- Assign the private data to the relevant variables inside the file: <b>AccountConfig.py</b>
- Look in the file <b>NovaScotiansBot.py</b>:
  - Look for: <code>user_defined_search_strings = ['Nova Scotia', 'Scotian']</code>
    - Replace <b>'Nova Scotia', 'Scotian'</b> with what keywords you want to get news for.
  - Look for: <code>this_bot_is_a_mod_and_will_cycle_a_monthly_chat_lounge = False</code>
    - Set it to <b>True</b> if the bot is a mod in the subreddit, and you want it to cycle a monthly <b>r/SubReddit Chat Lounge For MMM, YYYY</b> live sticky post.
    - This will occur every time a new month is detected when the value is set to True.
- Use <B>Python 3</B> to run <b>NovaScotiansBot.py</b>:
  - <code>python3 NovaScotiansBot.py </code>
  - The script will run on a loop:
    - Every 15 minutes if there are any posts in <b>Posts.csv</b> yet to be posted to reddit.
    - Every 1.5 hours if all posts have been posted to reddit (prevents excessive news API calls).
  - The script identifies if it has posted an article to reddit using <b>Posts.csv</b>, where the 1st column of data = '<b>Posted</b>'.
  - When a new day is detected, the script will move <b>Posts.csv</b> to <b>Posts.csv<i>yyyyMMdd</i></b> and begin a new <b>Posts.csv</b>.
  - The script will create a new <b>NovaScotiansBot.dat</b> file each loop, which stores persistient time data the program needs to work smoothly in case it's stopped and restarted. 
  - CTRL+C will terminate the script.
    - To avoid the small risk of data-loss when writing to <b>Posts.csv</b> and <b>NovaScotiansBot.dat</b>, be sure to only press CTRL+C when you see: '<b><i>Waiting to run again @ yyyy-MM-DD HH:mm:ss.fff (CTRL+C to QUIT)</i></b>'.
  
## Issues:
- You might have to install some libraries.
- Could cause a problem of reposting if you delete <b>Posts.csv</b>.
- Could cause a problem of not archiving the last day properly, or not posting the monthly Chat Lounge if you delete <b>NovaScotiansBot.dat</b>
- Might be a bit limited with free API accounts.
- You might forget to delete backup <i>Posts.csvyyyyMMdd</i> files, and they could build up to consume all your free space :(.


## ToDo's:
- Find a way to make sure only english language posts are posted.
- Add more News APIs.
