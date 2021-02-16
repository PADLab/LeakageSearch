import errno
import ftplib
import os
from os import path

# create a folder to keep the downloaded files
newFolder = 'files'

try:
    os.makedirs(newFolder)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

fileAmount = 10000

ftp = ftplib.FTP("10.0.0.122", "anonymous", "firefox@example.com")

for x in range(fileAmount):
    currFile = "file" + str(x) + ".txt"
    if currFile in ftp.nlst():
        ftp.retrbinary("RETR " + currFile, open(newFolder+"/"+currFile, 'wb').write)

ftp.quit()