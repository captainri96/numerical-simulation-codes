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
        df = pd.read_csv(f'node_{each}_removed_{distn[patt]}.csv')
        df = df.to_numpy()

        R = pd.DataFrame(df)
        R.to_csv(f'_node_{each}_removed_{distn[patt]}.csv',\
                 index=False, header = False ) 


