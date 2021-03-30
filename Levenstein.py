import os
import Levenshtein
import sys
import time
import numpy as np

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

def getLevenstein(list):

    # Define variables
    timeList, dataList = [], []
    senPath = "files"

    # import the sensitive files and read to array
    senString = ""
    senFiles = []
    for root, dirs, files in os.walk(r'files'):
        for file in files:
            with open(senPath + "/" + file, 'r') as fd:
                senString += (str(fd.read()) + " ")
            senFiles = senString.split(" ")

    exfilDataFull = []
    for obj in list:
        exfilDataFull += obj.data.split(" ")

    # specify current and max exfil files to search
    exfilMax = len(list)

    for x in range(1):
        exfilCurr = 0
        count = 0

        while(exfilCurr <= exfilMax):

            score = 0
            levData = []

            # exfilData = exfilDataFull[:exfilCurr]

            # get the run time
            start = time.time()

            for i in exfilDataFull:                             # loop through sensitive files
                Curr = TopDist("", "", 0)                       # create temp Levenstein object
                for j in senFiles:                              # loop through exfiltrated data
                    currDist = Levenshtein.distance(i, j)       # get Levenstein distance between the two
                    big = max(len(i), len(j))                   # get max number between the lengths of strings being compared
                    percent = (big - currDist) / big            # get percentage match value
                    if percent > Curr.dist:                     # compare current smallest distance to currently found distance
                        Curr.senData = i                        # if smaller -> set temp object's sendata to i
                        Curr.exfilData = j                      # if smaller -> set temp object's exfildata to j
                        Curr.dist = percent                     # if smaller -> set current distance as dist
                score += Curr.dist                              # adds smaller current distance to score (print out later)
                levData.append(Curr)

            # get end time
            end = time.time()

            if x == 0:
                timeList.append(end - start)
                dataList.append(exfilCurr)
            else:
                timeList[count] += (end - start)
                count = count + 1
            exfilCurr += 10

    match = score/len(exfilDataFull)
    print("Score: {}".format(match))

    for x in range(len(timeList)):
        timeList[x] = timeList[x] / 100

    timeList=np.array(timeList)
    return dataList, timeList
