# Some Fun Python APIs + Modules I've Used

> Ranging from image processing to retrieving posts on Reddit
---
## Image Processing

Using the [Moviepy module](https://moviepy.readthedocs.io/en/latest/), I wrote some functions to overlay videos on images, images on images, etc., as well as video concatenation and text overlay with the textwrap module.
- function(s):
  - `file_over_image`, supports imgs, vids, gifs
  - `concat_video`
  - `text_overlay`

---
## Discord, Youtube Data APIs

See my other repository on creating a Discord bot (to interface with the [Discord API](https://discordpy.readthedocs.io/en/stable/api.html)) and having that bot interact with the [Youtube Data API](https://developers.google.com/youtube/v3). I've written many useful functions to do almost anything + more with Youtube's Playlists in the Discord client.

---
## Reddit API

I've used the [Reddit API](https://www.reddit.com/dev/api/) to mass-retrieve posts/images for a given subreddit and store them (plus other info) in a `pandas.DataFrame`.
- I followed [this](https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c) article to set up the API in its complex process.
- function(s):
  - `get_subreddit`
  - `load_subreddit_data`
  - `generate_new_api_token`

---
## Other APIs

- ### Instagram API ([instaloader](https://instaloader.github.io))
  - You can use it get posts, stories, etc., so I've used it to retrieve any part of a post based on the shortcode in its url and an optional arg, `postnums`.
  - function(s):
    - `get_insta_post`


- ### Remove.bg API ([here](https://www.remove.bg/api#remove-background))
  - Revome.bg is a nice site that uses ML to remove the backgrounds of images, and has an API that I used just for that.
  - function(s):
    - `removebg`
    
---

***See respective .py files for specifics of each function / API***
