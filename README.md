uploadit
========

A configurable python script that automates the process of uploading a file to a web host and sharing it on one or more social media networks. The file that uploadit processes is called the target file.

The operation of uploadit revolves around the configuration file. When the script is run, it processes the target file according to the sections that are found in the configuration file.

## Getting Started
Clone the git repository
``` bash
git clone https://github.com/MusikPolice/uploadit.git
cd uploadit
```

Install the required libraries
``` bash
pip install -r requirements.txt
```

Generate a sample configuration file
``` bash
python uploadit.py -s uploadit.conf
```

Process a target file
``` bash
python uploadit.py -c uploadit.conf targetfile.mp3
```

## Configuration
Each section that is added to the configuration file causes a different task to be run against the target file. The tasks are run in the same order that their corresponding sections appear in the file.

### Mp3Tag
The Mp3Tag module automates the task of adding ID3 metadata to target files that contain mp3 audio. To use it, add a section similar to the following to your configuration file:
``` python
    [Mp3Tag]
    title='Another Episode of My Podcast'
    artist='Me'
    genre='Podcast'
```

Each of the options under the Mp3Tag section header is of the form `key=value` where *key* is the name of the ID3 tag that will be written to the target file and *value* is the thing that will be assigned to that tag.

The Mp3Tag module is backed by the [mutagen](https://code.google.com/p/mutagen/) multimedia tagging library, and supports all of the same ID3 tags. Here's a small subset of the available tags:
* album
* artist
* copyright
* date
* encodedby
* genre
* releasecountry
* title
* tracknumber
* website

Of course, you can find the entire set of available tags by opening up a Python interpreter and typing the following:
``` python
    >>from mutagen.easyid3 import EasyID3
    >>print EasyID3.valid_keys.keys()
```

## FTP Upload
We're still working on writing this module.

## Post to Tumblr
We're still working on writing this module.

## Post to Twitter
We're still working on writing this module.

## Post to Facebook
We're still working on writing this module.
