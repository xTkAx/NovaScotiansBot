# <u><i>NovaScotiansBot</i></u>
![NovaScotiansBot](https://github.com/xTkAx/NovaScotiansBot/assets/16578236/d650aed1-32bf-4d81-a835-d6816252a07c)

This repository contains <b>Python 3</b> code to drive a Nova Scotia news bot reddit account, [NovaScotiansBot](https://www.reddit.com/u/NovaScotiansBot/), which will scan news APIs for Nova Scotian related news articles, and then post them to https://www.reddit.com/r/NovaScotians/.  In addition, it can maintain a monthly Chat Lounge on the subreddit.

<b>This repository can be modified to become your very own subreddit news & monthly chat lounge bot, in 4 simple steps!</b>

## How To Use:
1. Set up an account for your bot & get API keys for all the following services:
   -  https://www.reddit.com (Reddit API) +
      - Find a subreddit to use the bot in (work with a mod, or make a new one).
      - Make the bot an approved user in the subreddit if the bot account karma is low (otherwise it may be limited to posting once every 15 minutes).
      - Make the bot a mod user if you want it to create and sticky a monthly Chat Lounge.
   -  https://www.mediastack.com (News API).
   -  https://www.thenewsapi.com (News API).
2. Open <b>NovaScotiansBotConfig.py</b>, and assign the relevant variables retrieved from the above step.
3. Look in the file <b>NovaScotiansBot.py</b>:
     - Look for: <code>user_defined_search_strings = ['Nova Scotia', 'Scotian']</code>.
       - Replace <b>'Nova Scotia', 'Scotian'</b> with what keywords you want to get news for.
   - Look for: <code>this_bot_is_a_mod_and_will_cycle_a_monthly_chat_lounge = False</code>.
     - Set it to <b>True</b> if the bot is a mod in the subreddit, and you want it to cycle a monthly '<b>r/SubReddit Chat Lounge For Month, YYYY</b>' live sticky post.
       - This will occur every time a new month is detected.
     - Leave it set to <b>False</b> if the bot is not a mod in the subreddit, or you don't want it to cycle a monthly Chat Lounge. 
   - Look for: <code>archive_posts_file = False</code>.
     - Set it to <b>True</b> if you would like to reset the <b>Posts.csv</b> every day.
       - When a new day is detected, the script will move <b>Posts.csv</b> to <b><i>yyyyMMdd.</i>Posts.csv</b> for archiving, and begin a new <b>Posts.csv</b>.
     - Leave it set to <b>False</b> if you want to store all posts in one <b>Posts.csv</b> file.
4. Use <B>Python 3</B> to run <b>NovaScotiansBot.py</b>:
   - <code>python3 NovaScotiansBot.py</code>.
   - The script will run on a loop:
     - Every 15 minutes if there are any posts in <b>Posts.csv</b> yet to be posted to reddit.
     - Every 1.5 hours if all posts have been posted to reddit (prevents excessive news API calls).
   - The script identifies and updates if and when it has posted an article to reddit using <b>Posts.csv</b>, by setting the 1st column of data to '<b>Posted</b>'.
   - If <code>this_bot_is_a_mod_and_will_cycle_a_monthly_chat_lounge = True</code> <b>OR</b> <code>archive_posts_file = True</code>, the script will save data to <b>NovaScotiansBot.dat</b> on each loop.  This stores persistent time data the program requires to work seamlessly with these options, in the event the run is stopped and restarted. 
     - If <u>both</u> are set to <code>False</code>, <b>NovaScotiansBot.dat</b> will be purged on program start, and will not be used.
   - CTRL+C will terminate the script.
     - To avoid the small risk of data-loss when writing to <b>Posts.csv</b> and <b>NovaScotiansBot.dat</b>, be sure to only press CTRL+C when you see: '<b><i>Waiting to run again @ yyyy-MM-DD HH:mm:ss.fff (CTRL+C to QUIT)</i></b>'.
  
## Issues:
- You might have to install some libraries.
- Could cause a problem of reposting if you delete <b>Posts.csv</b>.
- Could experience a problem of not archiving the last day, or not posting the monthly Chat Lounge, if you delete <b>NovaScotiansBot.dat</b>.
- Might be a bit limited with free API accounts.
- You might forget to trim <b>Posts.csv</b>, or delete archived <b>yyyyMMdd.Posts.csv</b> files, and they could build up to consume all your free space :(.


## ToDo's:
- Find a way to make sure only english language posts are posted.
- Add more News APIs.
