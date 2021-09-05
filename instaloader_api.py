import instaloader, os

# Simple class that allows you to pass in an instagram url shortcode as an argument to the only function (with optional post numbers if it's a post with slides)
# and will return the list of paths to each desired slide that the user requested. Left in some code to transform into Discord bot if wanted.

class instaloader_api:
  
  loader, loader_built = '', False # dummy vals
  
  def __init__(self):
    global loader, loader_built
    loader = ''
    loader_built = False

       
    
  def get_insta_post(self, shortcode, postnums=[]):
    global loader, loader_built
    
    if len(postnums) == 0: # get first post in potential slide of posts
      postnums = ['1']
    path = '~/path/to/storage/' # temporary place to store post(s) in case you want to delete them
    count = 1
    
    # creating instaloader instance and downloading the files if not already built
    if not loader_built:

      loader = instaloader.Instaloader(dirname_pattern=path, download_video_thumbnails=False, save_metadata=False, compress_json=False, download_comments=False, post_metadata_txt_pattern="", download_geotags=False) #creates instance
      loader.login('username', 'password')
      loader_built = True

    # actual line to load the post from Instagram
    try:
      postObj = loader.download_post(instaloader.Post.from_shortcode(loader.context, shortcode), target=shortcode)
    except Exception as e:
      return e # returns as string
    
    # send the specified post numbers
    if len(os.listdir(path)) == 1: # first post in potential slides of posts
      filename = os.listdir(path)[0]
#       await ctx.send(file = discord.File(path+filename, filename=filename))
      files.append(path+filename)

    else: # multiple files
      if '10' in postnums:
        postnums[postnums.index('10')] = '0'
        
      files = []
      for filename in sorted(os.listdir(path)):
        if filename[-5] in postnums: # add file to list of files to return
#           files.append(discord.File(path+filename))
          files.append(path+filename)
        count += 1
#       await ctx.send(files=files)

    # you'd usually want to automatically delete the files after you're done with them on a Discord bot, so I've included
    # the code to do that, but for normal applications you'll want to do something after the function finishes, so I've commented out the code
    # removing the file so that there's no trace left that i have to delete
#     try:
#       for filename in os.listdir(path):
#         os.remove(path+filename)
#       os.rmdir(path)
#       print('removed: ' + path)
#     except Exception as e:
#       print("Error: %s" % e.strerror)
#       return e
    
    # code for if you want to close the instaloader object after each call to the method
#     try:
#       loader.close()
#       print('loader closed')
#     except Exception as e:
#       print('error closing loader: ' + str(type(e).__name__))

    return files
  # end method
      
# end class
