# Some Fun Python APIs + Modules I've Used

> Ranging from image processing to retrieving posts on Reddit
---
## Image Processing

Using the [Moviepy module](https://moviepy.readthedocs.io/en/latest/), I wrote some functions to overlay videos on images, images on images, etc., as well as video concatenation
- function(s):
  - `image_over_image(top, bottom)`
  - `video_over_image(video, img)`
  - `concat_video(start, video)`

---
## Discord, Youtube Data APIs

See my other repository on creating a Discord bot (to interface with the [Discord API](https://discordpy.readthedocs.io/en/stable/api.html)) and having that bot interact with the [Youtube Data API](https://developers.google.com/youtube/v3). I've written many useful functions to do almost anything + more with Youtube's Playlists in the Discord client.

---
## Reddit API

I've used the [Reddit API](https://www.reddit.com/dev/api/) to mass-retrieve posts/images for a given subreddit and store them (plus other info) in a `pandas.DataFrame`.
- I followed [this](https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c) article to set up the API in its complex process.
- function(s):
  - `get_subreddit(subreddit)`
  - `load_subreddit_data(subreddits=None, method='hot', time='day', limit=25)`
  - `generate_new_api_token()`

---
## Other APIs

- ### Instagram API ([instaloader](https://instaloader.github.io))
  - You can use it get posts, stories, etc., so I've used it to retrieve any part of a post based on the shortcode in its url and an optional arg, `postnums`.
  - function(s):
    - `get_insta_post(shortcode, postnums=[])`


- ### Remove.bg API ([here](https://www.remove.bg/api#remove-background))
  - Revome.bg is a nice site that uses ML to remove the backgrounds of images, and has an API that I used just for that.
  - function(s):
    - `removebg(path_to_img)`
    
---

***See respective .py files for specifics of each function / API***
