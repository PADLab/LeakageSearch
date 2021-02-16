import errno
import ftplib
import os

from numpy import random

# initial folder and file setup
newFile = 'data'

try:
    os.makedirs(newFile)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

fileAmount = 10000

for x in range(fileAmount):
    file = open(newFile + '/file' + str(x) + '.txt', 'w')

# Uploading all the files to the FTP server
ftp = ftplib.FTP('10.0.0.122', 'Jack', 'W@llB@ll1717')

# generate a random number array
randArr = random.randint(999999999, size=10000)

# write a random number in the file and upload it to the FTP server
for x in range(fileAmount):
    currFile = '/file' + str(x) + '.txt'
    with open(newFile + currFile, 'w') as file:
        file.write(str(randArr[x]))
        file.close()

    # print(path.exists(newFile + currFile))
    with open(newFile + currFile, 'rb') as file:
        ftp.storbinary(f'STOR {currFile}', file)
        file.close()

ftp.quit()
