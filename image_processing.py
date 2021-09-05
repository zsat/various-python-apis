import moviepy.editor as mp
from PIL import Image, ImageSequence, ImageOps, ImageDraw, ImageFont
import textwrap # multiline writing
import discord # not needed if you just want the code to do 
from discord.ext import commands

# Code has been left in the format of a Discord Cog, which is a class with functions, mainly because the necessary code can easily be extracted
# and because there's a lot of workaround that was necessary to make the code usable for a Discord bot

class image_processing(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
  
  
  # This specific function was made to recreate the 'This is x' Spotify meme, by having the file be a png/jpg/mp4/gif and 
  # being able to customize the name of the person that gets replaced under the 'This is' part of the text at the top.
  # You can go to ~/images/thisistemplate.png to see the template itself to get a better understanding of what this method does.
  # Of course, you can take most of this code and change a few lines so that there's no text needed, or so that you can choose what
  # type of file gets placed under the first inputted file that this function takes.
  @commands.command(help='type: file_over_image <name> (and include img/gif/mp4)')
  async def file_over_image(ctx, *, name=None):
    path = '~/path/to/storage/'
            
    pic = ctx.message.attachments[0]
    picsuffix = pic.filename.split('.')[-1]
    bg, fg = '', ''

    if picsuffix not in ['mp4', 'gif']:
      await pic.save(path + 'spotifyinput.png') # PIL should convert to png automatically, useful when we .convert('RGBA') later
      picsuffix = 'png'
    else:
      await pic.save(path + 'spotifyinput.' + picsuffix)
    await ctx.message.delete()
    
    # next we'll process where the name should go if we were given a name
    if name is None:
      bgname = 'thisisdefault.png' # you'll have to make your own default, or you can just open thisistemplate.png and not write a name
      bg = Image.open(path + bgname)
    else:
      bgname = 'thisisname.png' # the file we'll save the written name under, will superimpose other file on top later
      bg = Image.open(path + 'thisistemplate.png')
      xmid, ymid, xspace, yspace = 640, 225, 1140, 155

      # generate our text
      fontsize = yspace # font point size for this font is about the num of y pixels itll take up
      draw = ImageDraw.Draw(bg)
      font = ImageFont.truetype("Montserrat-Bold.ttf", fontsize)

      # get pixels of text
      xlen, ylen = font.getsize(name.upper())

      # check ratios of lens to space available
      if xlen > xspace:
        txtpercent = xlen/xspace
        font = ImageFont.truetype("Montserrat-Bold.ttf", (int)(fontsize/txtpercent)) # too long so we'll have to minimize the font
      else:
        txtpercent = ylen/yspace

      txtx = xmid - (int)(xlen/txtpercent / 2)
      txty = ymid - (int)(ylen/txtpercent / 2)

      # actually writing the text
      draw.text((txtx, txty), name.upper(), (0,0,0), font=font)

      bg.save(path + 'thisisname.png')
    
    # we've saved the background and can now proceed to overlaying the other img/gif/mp4 on it
    bg = Image.open(path + bgname)    
        
    if str.lower(picsuffix) == 'mp4':
      fg = mp.VideoFileClip(path + 'spotifyinput.mp4')
    elif str.lower(picsuffix) == 'gif':
      fg = Image.open(path + 'spotifyinput.gif')
    else:
      fg = Image.open(path + 'spotifyinput.png')
        
    fgW, fgH = fg.size
    bgW, bgH = bg.size
    xmid, ymid, xspace, yspace = 640, 763, 1280, 775
        
    percent=0
    if (fgW/xspace) > (fgH/yspace): #if width goes over more than height
      percent = xspace/fgW
    else:
      percent = yspace/fgH
        
    x = xmid - (int)(fgW*percent/2)
    y = ymid - (int)(fgH*percent/2)
        
    # now just use our libs to process the format and overlay the img/gif/vid over our background img    
    if str.lower(picsuffix) == 'gif': # overlay gif
      scale_factor = 0.2
      image = mp.ImageClip(path + bgname)
      image = image.resize(scale_factor)
      video = mp.VideoFileClip(path + "spotifyinput.gif", resize_algorithm='lanczos')
      video = video.resize(percent*scale_factor)

      final = mp.CompositeVideoClip([image, video.set_position(((int)(x*scale_factor),(int)(y*scale_factor)))])
      final.duration = video.duration
      final.write_gif(path+"lastspotify.gif")

    elif str.lower(picsuffix) == 'mp4': # overlay video

      image = mp.ImageClip(path + bgname)
      video = mp.VideoFileClip(path + "spotifyinput.mp4")
      video = video.resize(height=(int)(fgH*percent))

      final = mp.CompositeVideoClip([image, video.set_position((x,y))])
      final.duration = video.duration
      final.write_videofile(path+"lastspotify.mp4")
        
    else: #is picture, lots of niche Googling was done here
      fg = fg.resize( size=((int)(fgW*percent) , (int)(fgH*percent)) )
      # if it isn't already rbg, could be grayscale which will make pic gray
      bg = bg.convert("RGBA")
      fg = fg.convert("RGBA")
      pic = Image.new("RGBA", bg.size)
      pic.paste(fg, (x,y))

      final = Image.new("RGBA", bg.size)
      final = Image.alpha_composite(final, bg)
      final = Image.alpha_composite(final, pic)
      final.save(path + 'lastspotify.png')

    file = discord.File(path + 'lastspotify.' + picsuffix)    
    await ctx.send(file=file)
  # end file_over_image


  
  
  
  # concatenates a pre-set video to the end of a provided file by the user, but can be easily changed so that
  # the user provides 2 files and the function will concatenate one onto the other
  @commands.command(help='concatenates a video to the end of provided')
  async def concat(self, ctx):
    path = '~/path/to/storage/' # path where you want to keep your videos

    # you can 'reply' to messages, so now you don't even need to post a file yourself, you can just like it to a command
    if ctx.message.reference is not None:
      in_vid = await ctx.channel.fetch_message(ctx.message.reference.message_id)
      in_vid = in_vid.attachments
    else: # else it was manually posted
      in_vid = ctx.message.attachments

    # if no video sent in or file isnt an mp4
    suffix = str.lower(in_vid[0].filename.split('.')[-1])
    if not in_vid or suffix not in ['mp4', 'png', 'jpg', 'jpeg']:
      await ctx.send('bad format: .'+suffix)
      await ctx.message.add_reaction("👎")
      return

    in_vid = in_vid[0]
    await in_vid.save(path + 'input.'+suffix)

    try: await ctx.message.delete()
    except Exception as e: print('couldn\'t delete message (likely no permission to do so)') 

    # create a time to cut off the video at, this uses 5 seconds but can be inputted easily
    if suffix == 'mp4':
      vid = mp.VideoFileClip(path + 'input.'+suffix)
      dur = vid.duration
      dur = dur if (dur < 5) else 5
      vid = vid.subclip(0, dur)
    else: # if it's an image, let play for 2.5 seconds
      vid = mp.ImageClip(path + 'input.'+suffix).set_duration(3)
      vid = vid.subclip(0.5, 3)

    # have a second video to auto concat, though this can easily be made to be a second input
    concat_vid = mp.VideoFileClip(path + 'concat_vid.mp4')
    # going to match the dimensions of the first video
    concat_vid = concat_vid.resize(vid.size)

    # actual concatenation
    final_video = mp.concatenate_videoclips([vid, concat_vid])
    final_video.write_videofile(path + 'last_video.mp4')

    await ctx.send(file=discord.File(path + 'last_video.mp4'), content='courtesy of '+ctx.author.name)
  # end concat

  
  
  
  
  # this is easily usable for an image that 
  @commands.command(help="captions the pre-set picture")
  async def text_overlay(self, ctx, *, text=None):
    path = '~/path/to/storage/'

    if text is None:
      await ctx.message.add_reaction("👎")
      await ctx.send('you didn\'t provide a caption')
      return

    text = ''.join(text)
    try:
      await ctx.message.delete()
    except Exception as e:
      print("failed to delete caption message")
      pass
    
    # next we'll process where the name should go if we were given a name
    bgname = 'presetbg.png'
    bg = Image.open(path + bgname)
    buffer = 40 # 40px buffer on each side, also where x will start
    xmid, y = 1210, 300

    # generate our text
    # you can change the font, position of text, width, fontsize, etc. to fit your image with a little work
    fontsize = 75 # font point size for this font is about the num of y pixels itll take up
    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype("Copperplate.ttc", fontsize)

    lines = textwrap.wrap(text, width=14)
    for line in lines:
      width, height = font.getsize(line)
      draw.text((xmid-(width/2), y), line, (0,0,0), font=font)
      y += height

    bg.save(path + 'lasttext_overlay.png')

    file = discord.File(path + 'lasttext_overlay.png')    
    await ctx.send(file=file, content='courtesy of '+ctx.author.name)
  # end text_overlay
  
# end class

# when called, adds functions to main runnable .py file that the bot uses  
def setup(bot):
  bot.add_cog(image_processing(bot))  
