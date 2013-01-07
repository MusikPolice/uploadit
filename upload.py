#! /usr/bin/python

# NOTE: This script requires the following libraries:
# 	paramiko	http://www.lag.net/paramiko/

from ftplib import FTP
import os
import string
import sys
import paramiko

newest = 0

for filename in os.listdir(os.path.abspath(".")):
	if filename[:3] > newest and filename[:3].isdigit():
		newest = filename

directory = os.path.abspath(".") + "/" + newest + "/"

for filename in os.listdir(os.path.abspath(directory)):
	if filename[-3::] == "mp3":
		uploadfile = directory + filename
		break

logfile = os.path.abspath(".") + "/upload.log";
paramiko.util.log_to_file(logfile)

print "Connecting to remote host..."
host = "linode.ev98.ca"
port = 55022
transport = paramiko.Transport((host, port))
password = "$@uced2010!"
username = "slightlysauced"
transport.connect(username = username, password = password)
sftp = paramiko.SFTPClient.from_transport(transport)

print "Uploading " + filename + "..."
sftp.put(uploadfile, "www/media/" + filename)

print "Closing remote host connection"
sftp.close()
transport.close()

print "Updating playlist file"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=host,port=port,username=username,password=password)

command = "echo \"/var/www/slightlysauced.com/media/" + filename + "\" >> /opt/shoutcast/playlists/sauced.lst"
stdin,stdout,stderr = ssh.exec_command(command)

print "Restarting ShoutCast"
command = "kill -s SIGUSR1 $(pgrep sc_trans)"
stdin,stdout,stderr = ssh.exec_command(command)
ssh.close()

print "Uploading to RantRadio"
ftp = FTP('ftp.rantradio.com')
ftp.login('slightlysauced','underit4')
f = open(uploadfile, "rb")
ftp.storbinary('STOR ' + 'slightlysauced.mp3', f)
f.close()
ftp.quit()

print "URL is http://media.slightlysauced.com/" + filename
