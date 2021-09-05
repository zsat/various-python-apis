import requests, random, time
import pandas as pd
from collections import deque

# This class will auto-update your API token if it is likely to be invalidated by Reddit. Its main function is to return a random picture/video from
# a specified or random subreddit. The user can specify that the program downloads data for a specific subreddit, or you can hardcode some default 
# subreddits into 'default_subs' so that no subreddit is required. In addition, if you've used up more than half of the first requests returned posts
# then the program'll fetch more posts from the past week. # Also useful for a discord bot where you can call a command and get a random post back.

# switch HTTP requests from the current requests module to AIOHTTP for asynchronous calls if you need
class reddit_api:
  
  REDDIT_TOKEN, reddit_headers, last_reddit_token_update, subreddits_df, default_subs, all_subs_deques, extended_subs = ['']*7
  
  
  def __init__(self):
    global REDDIT_TOKEN, reddit_headers, last_reddit_token_update, subreddits_df, default_subs, all_subs_deques, extended_subs

    REDDIT_TOKEN, reddit_headers, last_reddit_token_update, subreddits_df, all_subs_deques, extended_subs = '', '', 0, pd.DataFrame(), [], {}
    # list of default subreddits that will auto-load every time you call get_subreddits and the token has expired
    default_subs = ['pics', 'aww'] 
  
  
  
  
  
  
  # can specify subreddit, else will pick one from the list of defaults
  def get_subreddit(self, subreddit=None):
    global REDDIT_TOKEN, reddit_headers, last_reddit_token_update, subreddits_df, default_subs, all_subs_deques, extended_subs
    
    # get random subreddit if user doesn't specify
    subreddit = random.choice(default_subs) if (subreddit == None) else subreddit[0].lower()

    # make sure our token is valid
    if time.time() - last_reddit_token_update > 3000: # reddit invalidates each token after about an hour, if true then update token
      
      last_reddit_token_update = time.time()
      self.generate_new_reddit_token()
      
      if len(subreddits_df) == 0: # load all default sub data
        print('fetching default subreddit data...')
        num_posts_loaded = self.load_subreddit_data()
        print('loaded '+str(num_posts_loaded)+' posts from default subreddits')    


    # make sure we dont already have that subreddit in the dataframe
    # if we don't then load it and ensure we load more than zero posts
    if subreddit not in list(subreddits_df['subreddit'].unique()):  
      
        # make sure subreddit is valid
        res = requests.get("https://oauth.reddit.com/r/"+subreddit+"/hot", headers=reddit_headers)
        if res.status_code == 404:
          return 'that sub might not exist: '+str(res.status_code)+', '+res.reason)
        elif not res.ok:
          return 'something went wrong... '+str(res.status_code)+', '+res.reason)
          
        # response gave OK code
        print('loading hot posts from r/'+subreddit+'...')
        num_posts_loaded = self.load_subreddit_data(subreddit=subreddit)
        if num_posts_loaded == 0:
          return 'couldn\'t load any posts :('
        print('loaded '+str(num_posts_loaded)+' posts from r/'+subreddit)

    # token is valid and subreddit has been loaded, so pick a random one not in our deque
    sub_posts = subreddits_df[subreddits_df['subreddit'] == subreddit]
    post = sub_posts[~sub_posts['url'].isin(all_subs_deques[subreddit])].sample().iloc[0]

    # optional code if integrated into a Discord bot, sends image as an Embed    
#     link = ''
    if post is not None:
#       randhex = "0x%06x" % random.randint(0, 0xFFFFFF)
#       # can just add the url to the image field and discord will download and display the image so we dont have to
#       desc = '[from r/'+subreddit+'](https://new.reddit.com/'+post.link+')'
#       embed = discord.Embed(title=post.title[:256], description=desc, color=int(randhex,16))
#       if post.url.split('.')[-1] in ['png', 'jpg']:
#         embed.set_image(url=post.url)
#       else: # is video
#         link = post.url
#       embed.set_footer(text=str(int(post.ups))+' upvotes ('+str(int(post.ratio *100))+'%)')

#       if ctx.channel.id in [channel id's you want to send it directly to]:
#         if link != '':
#           await ctx.send(embed=embed, content=link)
#         else:
#           await ctx.send(embed=embed)
#         print('sent '+post.url+' to zekky dungeon')
#       else:
#         if link != '':
#           await ctx.author.send(embed=embed, content=link)
#         else:
#           await ctx.author.send(embed=embed)
#         print('sent '+post.url+' to '+ctx.author.name)

#       await ctx.message.add_reaction('👍')
      # end optional code
  
      # add to deque, see below for explanation
      all_subs_deques[subreddit].append(post.url)

      # keeping a deque for each subreddit so that we don't randomly send the same post within rapid succession
      # start emptying the deque if its length is half of the total posts we have under a subreddit
      deque_maxlen = int(len(subreddits_df[subreddits_df['subreddit'] == subreddit]) / 2)
      
      # if deque is full and more posts havent already been added
      if len(all_subs_deques[subreddit]) == deque_maxlen and subreddit not in extended_subs:
        
        print('adding new posts to r/'+subreddit+'...')
        num_added = self.load_subreddit_data(subreddit=subreddit, method='top', time='week', limit=50)
        print('added '+str(num_added)+' new posts to r/'+subreddit)

        # copy deque'd posts over to a larger deque
        temp = deque(maxlen = int(deque_maxlen*2 + (num_added / 2)) )
        for post in all_subs_deques[subreddit]:
          print('post : '+str(post))
          temp.append(post)
        all_subs_deques[subreddit] = temp.copy() # shallow copy but the id() of the two deques will be different so it works

        extended_subs.append(subreddit)
      else:
        return 'subreddit already extended'

      # returning the DataFrame entry for the post which contains info like the url, num upvotes, title, img url
      return post

    else: # post should never be None
        return 'Something went fatally wrong, try another subreddit'


        
            
    
    
    # load all default subreddit data or load a specific sub
  def load_subreddit_data(self, subreddit=None, method='hot', time='day', limit=25):
    global reddit_headers, subreddits_df, default_subs, all_subs_deques
    
    count = 0 # total posts we add, will be returned
    subs = default_subs if subreddit is None else [subreddit]
    
    #load subreddit(s)
    for sub in subs:
      res = requests.get("https://oauth.reddit.com/r/"+sub+"/"+method+"/?t="+time+"&limit="+str(limit), headers=reddit_headers)

      if not res.ok:
        print('got error code '+str(res.status_code)+' '+res.reason+' for r/'+sub)
      else:
        posts = res.json()['data']
        # loop through each post retrieved from GET request
      
        for post in posts['children']:
          post = post['data']
          if post['url'] not in list(subreddits_df['url']): # if unique post then try to add it

            # images and videos are stored differently so need to know where to look in the response for each link respectively
            content_url = ''
            if post['url'].split('.')[-1] in ['jpg', 'png']: # if image
              content_url = post['url']
            elif post['is_video']:
              content_url = post['media']['reddit_video']['fallback_url']
              print(content_url)

            if content_url != '':
              subreddits_df = subreddits_df.append({
                'subreddit' : post['subreddit'].lower(),
                'title' : post['title'],
                'url' : content_url,
                'link' : post['permalink'],
                'ratio' : post['upvote_ratio'],
                'ups' : post['ups'] }, ignore_index=True)
              count += 1
        # create a spot in our DataFrame
        if sub not in all_subs_deques:
          ml = int(len(subreddits_df[subreddits_df['subreddit'] == sub]) / 2)
          all_subs_deques[sub] = deque(maxlen = int(len(subreddits_df[subreddits_df['subreddit'] == sub]) / 2))
          print('maxlen for '+sub+' = '+str(ml))
    return count
  # end load_subreddit_data


  
  
  

  def generate_new_reddit_token(self):
    global REDDIT_TOKEN, reddit_headers, subreddits_df

    subreddits_df = pd.DataFrame(columns=['subreddit','title','url'])  # re-initialize dataframe
    auth = requests.auth.HTTPBasicAuth('FOLLOW', 'GUIDE') # follow this guide: https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
    data = {'grant_type': 'password', 'username': 'YOUR-USERNAME', 'password': 'YOUR-PASSWORD'}
    reddit_headers = {'User-Agent': 'YOUR-BOT-NAME/0.0.1'}
    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=reddit_headers)
    REDDIT_TOKEN = res.json()['access_token']
    # add authorization to our headers dictionary
    reddit_headers['Authorization'] = f"bearer {REDDIT_TOKEN}"
  # end generate_new_reddit_token

# end class
