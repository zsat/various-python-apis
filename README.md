# Some Fun Python APIs + Modules I've Used

> Ranging from image processing to retrieving info from Reddit
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

I've used the Reddit API to mass-retrieve posts/images for a given subreddit and store them (plus other info) in a `pandas.DataFrame`.
- function(s):
  - `asdf`
  - `load_subreddit_data(subreddits=None, method='hot', time='day', limit=25)`
  - `generate_new_api_token(self)`

---
## Other APIs

- ### Instagram API (instaloader)
  - You can use it get posts, stories, etc., so I've used to to retrieve any part of a post post based on the post's shortcode in its url and optional `args`.
  - function(s):
    + test
    + `get_insta_post(shortcode, *, postnums=None)`


- ### Remove.bg API
  - Revome.bg is a nice site that uses ML to remove the backgrounds of images, and has an API that I used just for that.
  - function(s):
    - `removebg()`
    
---

***see functions.py to see the specifics***
