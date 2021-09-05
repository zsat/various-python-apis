# Very useful in a Discord bot (like the one I made) because you can just upload an image with a command, and the bot can just return the finished image
# without the user having to deal with getting file paths

class removebg_api:
	
	def removebg(self, path_to_img):
    
    storage_path = '~/path/to/storage/' # path we want to store our finished images in
    suffix = str.lower(path_to_image.split('.')[-1]) # getting suffix so we can produce a separate file
        
		#	if this throws an exception then there's likely a problem opening the file, perhaps not a valid format
		try:
			response = requests.post(
    	'https://api.remove.bg/v1.0/removebg',
    	files={'image_file': open(path_to_img, 'rb')},
    	data={'size': 'auto'},
   	  headers={'X-Api-Key': 'YOUR-API-KEY'}, # follow the instructions here: https://www.remove.bg/api#remove-background
    	)
		except Exception as e:
			return e # returns as string
    
		# if all goes well, write the image to our designated storage path
    if response.status_code == requests.codes.ok:
        with open(storage_path + 'no-bg.'+suffix, 'wb') as out:
            out.write(response.content)
    else:
        print("Error:", response.status_code, response.text)
	# end removebg

# end removebg_api
