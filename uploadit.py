from ConfigParser import ConfigParser

import argparse
import logging
import os
import sys

from uploadit import mp3tag

class Uploadit():
	log = None

	def __init__(self):
		"""Starts the application."""
		self._init_logging()


	def process(self, path, config):
		"""Uses the options specified in config to process the file specified by path
			path: the path to the file that will be processed.
			config: a file object that has been opened for reading and contains configuration options.
		"""
		self.log.info("Processing the file %s with the configuration supplied in %s" % (path, config.name))

		conf = ConfigParser()
		conf.readfp(config)
		for section in conf.sections():
			self.log.debug("Found section %s" % section)

			if section == 'Mp3Tag':
				if not mp3tag.has_prerequisites():
					self.log.warning('Failed to import the required libraries for Mp3Tag functionality.')
					break
				mp3tag.Write(path, self.log, conf)


	def generate_default_config(self, config):
		"""Generates a default configuration file and writes it to the open file object specified by config"""
		self.log.info("Writing sample config file to %s" % config.name)

		conf = ConfigParser()
		conf.add_section('Mp3Tag')
		conf.set('Mp3Tag', 'metadata-file', 'metadata.txt')
		conf.set('Mp3Tag', 'title', 'Episode 1: Some Jerks Talk about Stuff')
		conf.set('Mp3Tag', 'artist', 'Podcasting Jerks')
		conf.set('Mp3Tag', 'album', 'Podcasting Jerks Podcast')
		conf.write(config)


	def _init_logging(self):
		"""Initializes the log object"""
		self.log = logging.getLogger('uploadit')
		self.log.setLevel(logging.DEBUG)

		# create a handler that dumps log messages to the console
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)
		ch.setFormatter(logging.Formatter('%(message)s'))
		self.log.addHandler(ch)

		# create a handler that dumps log messages to a log file
		log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploadit.log'))
		fs = logging.FileHandler(log_path)
		fs.setLevel(logging.DEBUG)
		fs.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
		self.log.addHandler(fs)


def _can_open_file_for_read(path):
	"""Opens the file specified by path for reading and immediately closes it.
	If the file does not exist or cannot be opened for reading, an argparse.ArgumentTypeError is thrown"""
	try:
		with open(path, 'r') as f: f.close()
		return path
	except:
		raise argparse.ArgumentTypeError('Could not open file %s for reading.' % path)


def _open_file_for_read(path):
	"""Opens the file specified by path for reading. Returns the opened file object.
	If the file does not exist or cannot be opened for reading, an argparse.ArgumentTypeError is thrown"""
	try:
		return open(path, 'r')
	except:
		raise argparse.ArgumentTypeError('Could not open file %s for reading.' % path)


def _open_file_for_write(path):
	"""Opens the file specified by path for writing. If the file does not exist, it will be created.
	Returns the opened file object. If the cannot be opened for writing or created, an
	argparse.ArgumentTypeError is thrown"""
	try:
		return open(path, 'w')
	except:
		raise argparse.ArgumentTypeError('Could not create or open file %s for writing.' % path)


if __name__ == '__main__':
	"""Application entry point"""
	parser = argparse.ArgumentParser(
		description='Processes FILE with the steps specified in CONFIG.',
		epilog='For more information, see https://github.com/MusikPolice/uploadit')

	# required - the file to be uploaded
	parser.add_argument('file',
		help='The file to be processed.',
		metavar='FILE',
		type=_can_open_file_for_read)

	parser.add_argument('-c', '--config',
		dest='config',
		nargs='?',
		const='uploadit.conf',
		default='uploadit.conf',
		help='The path to a readable configuration file. If not specified, the default file uploadit.conf will be used.',
		type=_open_file_for_read)

	parser.add_argument('-s', '--sample',
		dest='sample',
		nargs='?',
		help='Writes a sample configuration file that shows all available options to the specified file.',
		type=_open_file_for_write)

	#TODO: add options for specifying the log file and the metadata file

	u = Uploadit()
	args = parser.parse_args()
	if args.sample is not None:
		u.generate_default_config(args.sample)
	else:
		u.process(args.file, args.config)
