import pyshark
import os
import Levenshtein
import sys
import time
import numpy as np
import matplotlib.pyplot as plt

class TopDist:
    def __init__(self, senData, exfilData, dist):
        self.senData = senData
        self.exfilData = exfilData
        self.dist = dist
    def __repr__(self):
        return "Sensitive Data: {}, " \
               "Exfiltrated Data: {}, " \
               "Levenshtein Distance: {}" \
            .format(self.senData, self.exfilData, self.dist)
    def __str__(self):
        return  "Sensitive Data: {}, " \
                "Exfiltrated Data: {}, " \
                "Levenshtein Distance: {}" \
                .format(self.senData, self.exfilData, self.dist)


# define the paths
pathToPcap = "pcapFiles/FTP1000.pcapng"
senPath = "files"
exfilPath = 'exfilData'
count = 0
tDistList, timeList, dataList = [], [], []

# specify current and max exfil files to search
exfilMax = 1000
exfilCurr = 0

"""
# import the pcap file
FTPCap = pyshark.FileCapture(pathToPcap, display_filter="ftp-data")
FTPCap.load_packets()

# get filtered file
filteredCap = pyshark.FileCapture('pcapFiles/filteredFTP1000.pcap')
filteredCap.close()
"""

# import the sensitive files and read to array
senFiles = []
for root, dirs, files in os.walk(r'files'):
    for file in files:
        if file.endswith('.txt'):
            senFiles.append(file)

while(exfilCurr <= exfilMax):

    exfilData = []
    with open(exfilPath + "/exfil" + str(exfilCurr)+".txt", 'r') as fd:
        exfilData = " " + (str(fd.read().replace('\n', '')))

    exfilData = list(exfilData.split(" "))

    # append amount of data points searched
    dataList.append(exfilCurr)

    print("To Search: {}".format(exfilCurr))
    # compare the sensitive data to pcap file

    # get the run time
    start = time.time()

    for file in senFiles:
        Curr = TopDist("", "", sys.maxsize)
        #print("Start: {}".format(time.time()))
        with open(senPath + "/" + file, 'r') as fd:
            sData = fd.read().replace('\n', '').encode('utf-8')
            sHex = sData.hex()
            for pkt in range(exfilCurr):
                #command = str(filteredCap[pkt][6].__dict__.values())
                eData = exfilData[pkt]
                currDist = Levenshtein.distance(sHex, eData)
                #print("Comparing: {} with {} and got {}".format(sData, eData, currDist))
                if currDist < Curr.dist:
                    Curr.senData = sData
                    Curr.exfilData = eData
                    Curr.dist = currDist
            #print("End: {}".format(time.time()))
        fd.close()
        tDistList.append(Curr)
    print("Current Iteration Done: {} files checked".format(exfilCurr))
    exfilCurr+=50

    # get end time
    end = time.time()
    timeElapsed = end-start

    print("{} and {}".format(start, end))

    print("{} \n".format(timeElapsed))

    # append time for each iteration to list for graphing
    timeList.append(timeElapsed)

timeList=np.array(timeList)
plt.plot(dataList, timeList)
plt.show()
