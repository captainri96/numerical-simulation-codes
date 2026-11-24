import numpy as np
import pandas as pd
import csv

csV = int(input("Enter 0 for initial node 0 and 1 if you opt to choose 'ave' files: "))

patterns = ['Monocrop', 'Rows_Columns', 'Diagonal',\
            'Row strips', 'Column strips', 'Patches']

column_name =['Mono', 'Row','Diagonal', 'Row Strips', 'Column Strips','Patches']
row_name = ['\u03BB=1, \u03C3=2.5', '\u03BB=1, \u03C3=4', \
            '\u03BB=2, \u03C3=2.5', '\u03BB=2, \u03C3=4', \
            '\u03BB=5, \u03C3=2.5', '\u03BB=2, \u03C3=4']

row_name = ['lambda=1, sigma=2.5', 'lambda=1, sigma=4', \
            'lambda=2, sigma=2.5', 'lambda=2, sigma=4', \
            'lambda=5, sigma=2.5', 'lambda=5, sigma=4']

print(row_name)

sig = [2.5, 4] #insect mobility: # 1.0, 2.5, 4.0 -> poor mobility
lambd = [1, 2, 5]   #trap strength: 1.0, 2.0, 5 +inf  -> perfect trap strength
m, n, N = 19, 98, 1000

r_ave, row = np.zeros((6,6), dtype='f'), 0

for lambdA in lambd:
    for sigma in sig:
        if csV == 0:
            df1 = pd.read_csv(f"(0) Proportion of Removed at Equilib t_sigma={sigma}_lambda={lambdA}.csv")
        else:
            df1 = pd.read_csv(f"(ave)Proportion of Removed at Equilib t_sigma={sigma}_lambda={lambdA}.csv")
        r_i = df1.to_numpy()
        r_i = r_i[:,1:]
        
        for pattern in range(6):
            sum_r_i = 0
            pattern_name = patterns[pattern] 
            print(f'\nIntercropping pattern: {pattern_name}_ sigma={sigma},lambda={lambdA}')

            if pattern == 0:
                count = 1000
            else:
                count = 500

            sum_r_i = np.sum(r_i[:, pattern], axis=0)
            r_ave[row,pattern] = float(sum_r_i/count)
            
        row += 1
                
R_ave = pd.DataFrame(r_ave)
R_ave.columns = column_name
R_ave.index = row_name

if csV == 0:
    R_ave.to_csv(f"Percentage of Removed Plants_(0).csv")
else:
    R_ave.to_csv(f"Percentage of Removed Plants_(ave).csv")

print('\nDone!\n')
