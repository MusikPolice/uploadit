def has_mp3tag_prerequisites():
	"""Returns true if all prerequisites of the mp3tag module are avaialable on this system"""
	try:
		import mutagen
	except ImportError:
		return False
	else:
		return True