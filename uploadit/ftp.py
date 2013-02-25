import ftplib
import os
import sys

class Upload():
    log = None
    conf = None
    sizeWritten = 0.0
    totalSize = 0.0
    percentComplete = 0
    
    def __init__(self, path, log, config):
        self.log = log
        
        host = config.get("ftp","hostname")
        username = config.get("ftp","username")
        password = config.get("ftp","password")
        
        f = open(path, "rb")
        self.totalSize = os.path.getsize(path)
        filename = os.path.basename(path)
        
        # Connect to FTP
        try:
            log.debug("Connecting to FTP host %s",host)
            ftp = ftplib.FTP(host)
        except Exception:
            log.error("Unable to connect to %s. Please verify the \"host\" parameter in the config file.", host)
            return
        
        # Log in to FTP
        try:
            log.debug("Logging in to %s with username %s",host,username)
            ftp.login(username, password)
        except Exception:
            log.error("Login failed to %s. Please verify the \"username\" and \"password\" parameters in the config file.", host)
            return
        
        # Upload file
        try:
            log.debug("Uploading file %s", filename)
            ftp.storbinary("STOR " + filename, f, callback = self.updateProgress,blocksize=1024)
        except Exception:
            log.error("Failed to upload %s to %s. Please try again.", filename, host)
            return
        
        log.debug("%s successfully uploaded.", filename)
        file.close
        ftp.close()
        log.debug("Logged out of FTP.")
        
    def updateProgress(self,block):
        self.sizeWritten += 1024
        if(((self.sizeWritten / self.totalSize)*100) > self.percentComplete and self.percentComplete < 100):
            self.percentComplete += 1
            sys.stdout.write("Upload progress: %d%%   \r" % (self.percentComplete) )
            sys.stdout.flush()
            
            
    
   
        