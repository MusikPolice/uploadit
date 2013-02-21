from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

class Write():
	log = None
	conf = None

	def __init__(self, path, log, config):
		self.log = log

		# open the path for writes
		mp3 = MP3(path, ID3=EasyID3)

		# write any static metadata values that appear in the config file to the id3 tags	
		for option in config.options("Mp3Tag"):
			if option in EasyID3.valid_keys.keys():
				log.debug('Writing tag %s=%s' % (option,config.get('Mp3Tag', option)))
				mp3[option] = config.get('Mp3Tag', option)
			else:
				log.debug("Invalid tag: %s", option)
				
		# process episode-specific metadata keys

		# add each of the metadata tag
		mp3.save()