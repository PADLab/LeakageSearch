import string
import pyshark
import numpy as np
import os
import sys
import csv
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import pandas as pd

# run tfidf on the sensitive data
# run tfidf on the exfiltrated data
# use cosine similarity to see which sensitive data document most matches with the query

def removePunc(text):
    text = "".join([ch for ch in text if ch not in string.punctuation])
    return text

# define the paths
pathToPcap = "pcapFiles/FTP1000.pcapng"
exfilData = ""
senPath = "files"
exfilPath = 'exfilData'

# specify current and max exfil files to search
exfilMax = 1000
exfilCurr = 0

# create the time complexity lists for graphing
timeList, dataList = [], []


#import the pcap file
FTPCap = pyshark.FileCapture(pathToPcap, display_filter='ftp-data')
FTPCap.load_packets()

for pkt in FTPCap:
    # put exfiltrated data into one string (query)
    try:
        command = str(pkt.layers[6]._all_fields.values())
        #print(command)
        if "RETR" in command:
            content = pkt["DATA-TEXT-LINES"]._all_fields
            for value in content.values():
                exfilData += " " + str(value)
    except KeyError:
        pass

FTPCap.close()


while(exfilCurr <= exfilMax):
    tmpList = []
    tmpList = list(exfilData.split(" "))  # convert to list
    tmpList = tmpList[:exfilCurr]  # cut list
    tmpString = ' '.join(tmpList)  # convert back to string
    currFile = '/exfil' + str(exfilCurr) + '.txt'
    with open(exfilPath + currFile, 'w+') as file:
        file.write(tmpString)
        file.close()
    print("Done with file exfil{}.txt".format(exfilCurr))
    exfilCurr+=50

# import the sensitive files and read to list
senData = ""
for root, dirs, files in os.walk(r'files'):
    for file in files:
        if file.endswith('.txt'):
            with open(senPath + "/" + file, 'r') as fd:
                senData += " " + str(fd.read().replace('\n', ''))

exfilCurr=0

while(exfilCurr <= exfilMax):

    print("Start! {}".format(exfilCurr))
    # import the sensitive files and read to list
    exfilData = ""
    with open(exfilPath + "/exfil" + str(exfilCurr)+".txt", 'r') as fd:
        exfilData = " " + str(fd.read().replace('\n', ''))

    combinedData=[exfilData, senData]

    # start recording the time
    start = time.time()

    vectorizer = TfidfVectorizer(stop_words='english', use_idf=True)

    # append amount of data points searched
    X = vectorizer.fit_transform(combinedData)

    pairwise_similarity = X * X.T

    pairwise_similarity.toarray()

    end = time.time()
    print(pairwise_similarity)

    dataList.append(exfilCurr)
    exfilCurr+=50

    print(end-start)
    timeList.append(end - start)

timeList=np.array(timeList)
plt.plot(dataList, timeList)
plt.show()

'''
vectorizer = TfidfVectorizer(stop_words='english')

while exfilCurr <= exfilMax:
    # start recording the time
    start = time.time()
    # append amount of data points searched
    X = vectorizer.fit_transform(filData[:exfilCurr])

    dataList.append(exfilCurr)
    data = removePunc(sHex)
    query_vec = vectorizer.transform([data])
    results = cosine_similarity(X, query_vec).reshape((-1,))
    exfilCurr+=10
    #for i in results.argsort()[-10:][::-1]:
        #print("Document {} -- {} -- Cosine similarity: {:.4f}".format(i+1, exfilData[i], results[i]))
    # stop the time and print
    end = time.time()
    timeList.append(end-start)

#print(*timeList, sep="\n")
timeList=np.array(timeList)
plt.plot(dataList, timeList)
plt.show()
#print("Time elapsed {:.2f} seconds".format(end-start))

'''








