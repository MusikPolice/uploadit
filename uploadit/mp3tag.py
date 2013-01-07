from mutagen.easyid3 import EasyID3

class Write():
	log = None
	conf = None

	def __init__(self, path, log, config):
		self.log = log

		# open the path for writes
		mp3 = EasyID3(path)

		# write any static metadata values that appear in the config file to the id3 tags
		for key in EasyID3.valid_keys.keys():
			if config.has_option('Mp3Tag', key):
				log.debug('Writing tag %s=%s' % (key,config.get('Mp3Tag', key)))
				mp3[key] = config.get('Mp3Tag', key)

		# process episode-specific metadata keys

		# add each of the metadata tags
		mp3.save()