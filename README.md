# <u><i>NovaScotiansBot</i></u>
![NovaScotiansBot](https://github.com/xTkAx/NovaScotiansBot/assets/16578236/d650aed1-32bf-4d81-a835-d6816252a07c)

This repository contains the <b>Python 3</b> code required to drive the Nova Scotia news bot Reddit account, [NovaScotiansBot](https://www.reddit.com/u/NovaScotiansBot/).

The <b>NovaScotiansBot</b> will scan news APIs for Nova Scotian related news articles, and then post them to https://www.reddit.com/r/NovaScotians/.  It will also cycle a monthly chat lounge sticky post on the subreddit <i>(provided the account is a moderator on the subreddit)</i>.

<b>This repository can be modified to make your very own subreddit news & monthly chat lounge bot.  All you need to do is follow the steps below!</b>

## How To Use:
1. Set up an account for your bot & get the API keys for all the following services:
   -  https://www.Reddit.com <i>(Reddit API)</i> +
      - Find a subreddit to use the bot in <i>(work with a moderator, or make a new subreddit and become the moderator of it)</i>.
      - <i>(Optional)</i>: Make the bot an approved user in the subreddit if the bot account karma is low <i>(otherwise it may be limited to posting once every 15 minutes)</i>.
      - <i>(Optional)</i>: Make the bot a moderator of the subreddit if you want it to cycle a stickied monthly Chat Lounge in the subreddit <i>(more about this below)</i>.
   -  https://www.mediastack.com <i>(News API)</i>.
   -  https://www.thenewsapi.com <i>(News API)</i>.


2. Open the file <b>NovaScotiansBotConfig.py</b>, and assign the relevant variables retrieved from the above step.
All fields will be checked by their respective APIs before being used, meaning if you don't fill the fields, the API related to those fields will not be used <i>(you can take advantage of this to skip APIs you don't want to use)</i>.


3. Open the file <b>NovaScotiansBot.py</b>:
     - Look for the following code:<br/><code>user_defined_search_strings = ['Nova Scotia', 'Scotian']</code>
       - Replace <b>'Nova Scotia', 'Scotian'</b> with what keywords you want to search and get news for <i>(each term or phrase surrounded by single quotes is a distinct search query)</i>.
   - Look for the following code:<br/><code>this_bot_is_a_mod_and_will_cycle_a_monthly_chat_lounge = False</code>
     - Set it to <b>True</b> if the bot is a moderator in the subreddit, and you want it to cycle a monthly '<b>r/SubReddit Chat Lounge For Month, YYYY</b>' live sticky post.  This will occur every time a new month is detected, and all articles from <b>NovaScotiansPosts.csv</b> have been posted to Reddit.  Once both of these conditions are met, the bot will identify the last Chat Lounge sticky it made, unstick it, create a new Chat Lounge for the current month <i>(with a link to the last month's Chat Lounge)</i>, and sticky the new post to the top of the subreddit.  
       - If the bot is not a moderator it will not be able to unstick and sticky a post, but it may create a Chat Lounge in the subreddit <i>(haven't really tested this much)</i>.
     - Leave it set to <b>False</b> if the bot is not a moderator in the subreddit, or you don't want it to cycle a monthly Chat Lounge. 
   - Look for the following code:<br/><code>archive_posts_file = False</code>
     - Set it to <b>True</b> if you would like to reset the <b>NovaScotiansPosts.csv</b> every day.  This will occur when a new day is detected and all articles from the file have been posted to Reddit.  Once these conditions are met, the application will move <b>NovaScotiansPosts.csv</b> to <b><i>yyyyMMdd.</i>NovaScotiansPosts.csv</b> for archiving, and begin storing subsequent discovered articles to a new <b>NovaScotiansPosts.csv</b> file until the next day.
     - Leave it set to <b>False</b> if you want to store all articles in one <b>NovaScotiansPosts.csv</b> file.


4. Use <B>Python 3</B> to run <b>NovaScotiansBot.py</b>:
   - <code>python3 NovaScotiansBot.py</code>.
   - The application will run on a loop:
     - Every 15 minutes if there are any articles in <b>NovaScotiansPosts.csv</b> yet to be posted to Reddit.
     - Every 1.5 hours if all articles have been posted to Reddit <i>(this prevents excessive news API calls)</i>.
   - The application overwrites <b>NovaScotiansPosts.csv</b> when it finds new articles and posts them to Reddit. Posted articles are identified in the file where the 1st column of data is  '<b>Posted</b>'.
   - If you set either of these values to <code>True</code>:<br/><code>this_bot_is_a_mod_and_will_cycle_a_monthly_chat_lounge = True</code><br/><b>OR</b><br/><code>archive_posts_file = True</code><br/>Then the application will store a persistent date value to <b>NovaScotiansBot.dat</b> on each loop.  The application requires this value to work seamlessly with those options in the event the run is stopped and restarted. 
     - If <u>both</u> are set to <code>False</code>, <b>NovaScotiansBot.dat</b> will be purged on application start, and will not be used.
   - <b>CTRL+C</b> can be used to terminate the application at any time. But to avoid the small risk of data-loss when writing to <b>NovaScotiansPosts.csv</b> and <b>NovaScotiansBot.dat</b>, it's best to wait until you see the application output this to the screen:<br/><code><b><i>..</code><br/><code>Waiting to run again in ### seconds, @ yyyy-MM-DD HH:mm:ss.ffffff</code><br/><code>(CTRL+C to QUIT)</i></b></code>
  
## Issues:
- You might have to install some libraries.
- Could cause a problem of reposting if you delete <b>NovaScotiansPosts.csv</b>.
- Could experience a problem of not archiving the last day, or not posting the monthly Chat Lounge, if you delete <b>NovaScotiansBot.dat</b>.
- Might be a bit limited with free API accounts.
- You might forget to trim <b>NovaScotiansPosts.csv</b>, or delete archived <b>yyyyMMdd.NovaScotiansPosts.csv</b> files, and they could build up to consume all your free space :(.


## ToDo's:
- Find a way to make sure only english language news articles are posted.
- Add more News APIs.
