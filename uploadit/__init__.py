def has_mp3tag_prerequisites():
	"""Returns true if all prerequisites of the mp3tag module are available on this system"""
	try:
		import mutagen
	except ImportError:
		return False
	else:
		return True
	
def has_sftp_prerequisites():
	"""Returns true if all prerequisites of the sftp module are available on this system"""
	try:
		import pysftp
	except ImportError:
		return False
	else:
		return True