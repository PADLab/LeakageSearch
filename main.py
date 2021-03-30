from getExfil import *
from getRedunElim import *
from TFIDF import *
from Levenstein import *
from graph import *
from match import *

'''
GENERAL PLAN:

1) call getExfil sending .pcap file return object list
2) call getRedunElim sending object list return object list
3) call FTPNGrams sending object list return two lists
4) call FTPSearch sending object list return two lists
5) call graphing function sending all lists print graphs
'''

# start pipeline

# call getExfil
print("Getting Footprint...")
day1, day2 = getExfil()
print("Done")

# call getRedunElim
print("Redundancy Elimination...")
uniqueListDay1 = unique(day1)
uniqueListDay2 = unique(day2)
print("Done")

# call findDiff
print("Finding Difference between two lists...")
diffList = findDiff(uniqueListDay1, uniqueListDay2)
print("Done")

# call getTFIDF
print("Getting TFIDF...")
dataListTFIDFdiff, timeListTFIDFdiff = getTFIDF(diffList)
dataListTFIDFday1, timeListTFIDFday1 = getTFIDF(uniqueListDay1)
dataListTFIDFday2, timeListTFIDFday2 = getTFIDF(uniqueListDay2)
print("Done")

# call getLevenstein
print("Getting Levenstein Distance")
dataListLevdiff, timeListLevdiff = getLevenstein(diffList)
dataListLevday1, timeListLevday1 = getLevenstein(uniqueListDay1)
dataListLevday2, timeListLevday2 = getLevenstein(uniqueListDay2)
print("Done")

"""

# graph the functions
print("Graphing...")
graph(dataListTFIDFdiff, timeListTFIDFdiff, dataListLevdiff, timeListLevdiff)
graph(dataListTFIDFday1, timeListTFIDFday1, dataListLevday1, timeListLevday1)
graph(dataListTFIDFday2, timeListTFIDFday2, dataListLevday2, timeListLevday2)
print("Done")

"""