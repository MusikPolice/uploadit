def has_prerequisites():
	"""Returns true if all prerequisites of the mp3tag module are avaialable on this system"""
	try:
		import mutagen
	except ImportError:
		return False
	else:
		return True


class Write():
	log = None
	conf = None

	def __init__(self, path, log, config):
		self.log = log
		self.config = config

		has_prerequisites()

		# open the path for writes

		# add each of the metadata tags