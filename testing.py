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
from scapy.all import *

# run tfidf on the sensitive data
# run tfidf on the exfiltrated data
# use cosine similarity to see which sensitive data document most matches with the query

def removePunc(text):
    text = "".join([ch for ch in text if ch not in string.punctuation])
    return text

# define the paths
pathToPcap = "pcapFiles/FTP1000.pcapng"
exfilData = []
pathToFiles = "files"

# specify current and max exfil files to search
exfilMax = 1000
exfilCurr = 0

#exfilData.append([str(pkt["DATA"]._all_fields["data"])])

# create the time complexity lists for graphing
timeList, dataList = [], []

pkts = sniff(offline='pcapFiles/FTP1000.pcapng', filter="TCP")

print(pkts)

preEnd = time.time()

preTime = preEnd

# import the sensitive files and read to list
sendata = ""
for root, dirs, files in os.walk(r'files'):
    for file in files:
        if file.endswith('.txt'):
            with open(pathToFiles + "/" + file, 'r') as fd:
                sendata += " " + str((fd.read().replace('\n', '')))

sHex = sendata.encode("utf-8").hex()

"""
vectorizer = TfidfVectorizer(stop_words='english', use_idf=True)

# start recording the time
start = time.time()
# append amount of data points searched
X = vectorizer.fit_transform(filData)
df = pd.DataFrame(X[0].T.todense(),
index=vectorizer.get_feature_names(), columns=["TF-IDF"])
df = df.sort_values('TF-IDF', ascending=False)
print (df.head(20))


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
"""