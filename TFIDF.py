import numpy as np
import time
import os
from sklearn.feature_extraction.text import TfidfVectorizer

def getTFIDF(uList):

    # define the paths
    senPath = "files"
    exfilPath = 'exfilData'

    # specify current and max exfil files to search
    exfilMax = len(uList)
    exfilCurr = 0
    exfilData = ""

    # create the time complexity lists for graphing
    timeList, dataList= [], []

    # put exfiltrated unique data into one string
    for obj in uList:
        exfilData += obj.data+" "

    # split exfil string into different sized files for testing
    while(exfilCurr <= exfilMax):
        tmpList = list(exfilData.split(" "))                    # convert to list
        tmpList = tmpList[:exfilCurr]                           # cut list
        tmpString = ' '.join(tmpList)                           # convert back to string
        currFile = '/exfil' + str(exfilCurr) + '.txt'           # set the correct file to open
        with open(exfilPath + currFile, 'w+') as file:          # open file
            file.write(tmpString)                               # write the exfil data to file
        exfilCurr+=10                                           # increase limit

    # import the sensitive files and read to list
    senData = ""
    for root, dirs, files in os.walk(r'files'):
        for file in files:
            with open(senPath + "/" + file, 'r') as fd:
                senData += " " + str(fd.read().replace('\n', ''))

    print(senData)

    for x in range(1):
        exfilCurr = 0
        count = 0
        while(exfilCurr <= exfilMax):
            # import the sensitive files and read to list
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

            if x == 0:
                timeList.append(end - start)
                dataList.append(exfilCurr)
                exfilCurr += 10
            else:
                timeList[count] += (end-start)
                count = count + 1
                exfilCurr += 10

    for x in range(len(timeList)):
        timeList[x] = timeList[x]/1

    print(pairwise_similarity)

    timeList=np.array(timeList)
    return dataList, timeList
