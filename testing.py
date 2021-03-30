import os

# import the sensitive files and read to array
senFiles = ""
senPath = "testingFiles"

for root, dirs, files in os.walk(r'testingFiles'):
    for file in files:
        with open(senPath + "/" + file, 'r') as fd:
            senFiles += str(fd.read()) + " "
        senFilesList = senFiles.split(" ")

print(senFilesList)