import numpy as np
import csv
import pandas as pd

print("\nHere is a list of the different cropping arrangements:\n")
distn = {0:'Monocrop', 1:'Rows', 2:'Diagonal',\
         3:'Row strips', 4:'Column strips', 5:'Patches'}
print(distn)

c_nodes = [13, 25,37,49,401,413,425,437,449,801,813,825,837,849]
patterN = [2, 4] # 2:'Diagonal' # 4:'Column strips'
m, n, N, t, count = 19, 98, 1000, 100, 0

for patt in patterN:
    for each in c_nodes:
        remov = np.zeros((N,t), dtype='f')
        for i in range(N):
            df = pd.read_csv(f'removed_set_{i}_{distn[patt]}_prcc.csv')
            prob = df.to_numpy()
            prob = prob[:,1:]

            remov[i,:] = prob[each-1, :]
            print(f'node {each} ({distn[patt]}): set {i}')

        R = pd.DataFrame(remov)
        R.to_csv(f'node_{each}_removed_{distn[patt]}.csv',\
                 index=False, header = False)

        

            
        
        
