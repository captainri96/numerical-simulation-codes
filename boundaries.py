import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import os
import itertools
import random

#os.system('cls')

"""MAIN"""

print("\nHere is a list of the different cropping arrangements:\n")
distn = {0:'Monocrop', 1:'Rows_Columns', 2:'Diagonal',\
         3:'Row strips', 4:'Column strips', 5:'Patches'}
print(distn, "\n")

column_name =['Mono', 'Ro_Cols','Diag', 'RowStps', 'ColStps','Pat']

df1 = pd.read_csv(r'Trap_crops_20_by_50_field.csv')
trap_ = df1.to_numpy()
traps = trap_[:,1:]   #traps.shape -> (1000,6)

#Boundary Points
boundary = []
b1_bottom, b1_top = [i for i in range(50)], [950+i for i in range(50)]
b1_left, b1_right = [(50+50*i) for i in range(18)], [(99+50*i) for i in range(18)]
boundary = list(itertools.chain(b1_bottom, b1_top, b1_left, b1_right))
boundary = np.array(boundary, dtype=int)

#Secondary Layer
layer_2 = []
s2_bottom, s2_top = [51+j for j in range(48)], [901+j for j in range(48)]
s2_left, s2_right = [(101+50*j) for j in range(16)], [(148+50*j) for j in range(16)]
layer_2 = list(itertools.chain(s2_bottom, s2_top, s2_left, s2_right))
layer_2 = np.array(layer_2, dtype=int)

#Third Layer
layer_3 = []
t3_bottom, t3_top = [102+j for j in range(46)], [852+j for j in range(46)]
t3_left, t3_right = [(152+50*j) for j in range(14)], [(197+50*j) for j in range(14)]
layer_3 = list(itertools.chain(t3_bottom, t3_top, t3_left, t3_right))
layer_3 = np.array(layer_3, dtype=int)

##print("\n", boundary, "\n", len(boundary))
##print(layer_2, "\n", len(layer_2))
##print(layer_3, "\n", len(layer_3))

#Mono, Ro_Cols, Diag, RowStps, ColStps, Patches

#nodes for the 100 realizations for each pattern
rea_RoCols, rea_Diag, rea_RowStps, rea_ColStps, rea_Patch = [], [], [], [], []
realizations = np.zeros((100,6), dtype=int)

for pattern in range(1,6):
    trap_nodes = traps[:, pattern]
    realiz = []
    print("\npattern:", distn[pattern])
 
    for node in boundary:
        if trap_nodes[node] != np.inf:
            realiz.append(node) #has 68 nodes in total

    laye_2 = []
    for node in layer_2:
        if trap_nodes[node] != np.inf:
            laye_2.append(node) #has 64 nodes in total
    #randomly selects 32 samples from all nodes in layer 2
    realiz.extend(random.sample(laye_2, 32)) 

    for j in range(100):
        realizations[j,pattern] = realiz[j]


    if pattern == 1:
        rea_RoCols = realiz
        print(len(rea_RoCols),'\n',rea_RoCols)
    elif pattern == 2:
        rea_Diag = realiz
        print(len(rea_Diag),'\n',rea_Diag)
    elif pattern == 3:
        rea_RowStps = realiz
        print(len(rea_RowStps),'\n',rea_RowStps)
    elif pattern == 4:
        rea_ColStps = realiz
        print(len(rea_ColStps),'\n',rea_ColStps)   
    else:
        rea_Patch = realiz
        print(len(rea_Patch),'\n',rea_Patch)


realizations[:,0] = realizations[:,1]



rand_realizations = pd.DataFrame(realizations, columns = column_name)
rand_realizations.to_csv(f'Nodes for the 100 random realizations.csv')




##traps = pd.DataFrame(secondary)
##traps.to_csv(f'Trap_crops_{m+1}_by_{total_row_nodes}_field.csv')


##common_boundary = []
##for node in rea_RoCols:
##    if (node in rea_Diag) == True:
##        if (node in rea_RowStps) == True:
##            if (node in rea_ColStps) == True:
##                if (node in rea_Patch) == True:
##                    common_boundary.append(node)
##print("\ncommon_boundary: \n",common_boundary)



