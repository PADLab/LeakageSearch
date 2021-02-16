import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

try:
    csvFile = sys.argv[1]
    df = pd.read_csv(csvFile)

except FileNotFoundError:
    print("File could not be found")
except IndexError:
    print("A file path must be added")

#df = pd.read_csv("C:/Users/Jack/Downloads/custom_normal.csv")

SrsIP = df['Src IP']
DstIP = df['Dst IP']

lst = zip(SrsIP, DstIP)

default_weight = 1
G1 = nx.DiGraph()
G2 = nx.DiGraph()
for nodes in lst:
    n0 = nodes[0]
    n1 = nodes[1]
    if G1.has_edge(n0+" Send",n1+ " Receive"):
        G1[n0+" Send"][n1+ " Receive"]['weight'] += default_weight
    elif G2.has_edge(n0+" Send",n1+ " Receive"):
        G2[n0 + " Send"][n1 + " Receive"]['weight'] += default_weight
    elif G1.has_edge(n1+" Send", n0+" Receive"):
        G2.add_edge(n0+" Send",n1+" Receive", color='b', weight=default_weight)
    else:
        G1.add_edge(n0+" Send", n1+" Receive", color='r', weight=default_weight)

colorsG1 = nx.get_edge_attributes(G1,'color').values()
#weightsG1 = nx.get_edge_attributes(G1,'weight').values()

colorsG2 = nx.get_edge_attributes(G2,'color').values()
#weightsG2 = nx.get_edge_attributes(G2,'weight').values()

pos1 = nx.circular_layout(G1)
pos2 = nx.circular_layout(G2)

nx.draw(G1, pos1,
        edge_color=colorsG1,
        #width=list(weightsG1),
        with_labels=True,
        node_color='lightgreen')

edge_labels=dict([((u,v,),d['weight'])
for u,v,d in G1.edges(data=True)])

nx.draw_networkx_edge_labels(G1,pos1,edge_labels=edge_labels)

plt.show()

nx.draw(G2, pos2,
        edge_color=colorsG2,
        #width=list(weightsG2),
        with_labels=True,
        node_color='lightgreen')

edge_labels=dict([((u,v,),d['weight'])
for u,v,d in G2.edges(data=True)])

nx.draw_networkx_edge_labels(G2,pos2,edge_labels=edge_labels)

plt.show()



