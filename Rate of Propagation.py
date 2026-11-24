import numpy as np
import pandas as pd
import csv

csV = int(input("\nEnter 0 for initial node 0 and 1 if you opt to choose 'ave' files: "))

patterns = ['Monocrop', 'Rows_Columns', 'Diagonal',\
            'Row strips', 'Column strips', 'Patches']

column_name =['Mono', 'Row','Diagonal', 'Row Strips', 'Column Strips','Patches']
##row_name = ['\u03BB=1, \u03C3=2.5', '\u03BB=1, \u03C3=4', \
##            '\u03BB=2, \u03C3=2.5', '\u03BB=2, \u03C3=4', \
##            '\u03BB=5, \u03C3=2.5', '\u03BB=2, \u03C3=4']

row_name = ['lambda=1, sigma=2.5', 'lambda=1, sigma=4', \
            'lambda=2, sigma=2.5', 'lambda=2, sigma=4', \
            'lambda=5, sigma=2.5', 'lambda=5, sigma=4']

print(row_name)

sig = [2.5, 4] #insect mobility: # 1.0, 2.5, 4.0 -> poor mobility
lambd = [1, 2, 5]   #trap strength: 1.0, 2.0, 5 +inf  -> perfect trap strength
m, n, N = 19, 98, 1000

rate, row = np.zeros((6,6), dtype='f'), 0

df = pd.read_csv(r'Trap_crops_20_by_50_field.csv')
trap_ = df.to_numpy()
traps = trap_[:,1:]

for lambdA in lambd:
    for sigma in sig:
        if csV == 0:
            df1 = pd.read_csv(f"(0) Proportion of Removed at Equilib t_sigma={sigma}_lambda={lambdA}.csv")
        else:
            df1 = pd.read_csv(f"(ave)Proportion of Removed at Equilib t_sigma={sigma}_lambda={lambdA}.csv")
        df2 = pd.read_csv(f"Equilibrium time T_sigma={sigma}_lambda={lambdA}.csv")

        r_i, t_e = df1.to_numpy(), df2.to_numpy()
        r_i, t_e = r_i[:,1:], t_e[:,1:]
        
        for pattern in range(6):
            pattern_name = patterns[pattern]
            print(f'\nIntercropping pattern: {pattern_name}_ sigma={sigma},lambda={lambdA}')

            if pattern == 0:
                count = 1000
            else:
                count = 500

            sum_wi_vi = 0
            sum_r_i = np.sum(r_i[:,pattern], axis=0)
            
            for node in range(N):
                if traps[node, pattern] != np.inf:
                    wi = r_i[node, pattern] / sum_r_i
                    vi = r_i[node, pattern] / t_e[node, pattern]

                    sum_wi_vi += (wi*vi)
                
            rate[row,pattern] = float(sum_wi_vi*count)
            
        row += 1
             
Rate = pd.DataFrame(rate)
Rate.columns = column_name
Rate.index = row_name

if csV == 0:
    Rate.to_csv(f"Rate of Propagation_dat_(0).csv")
else:
    Rate.to_csv(f"Rate of Propagation_dat_(ave).csv")


print('\nDone!\n')
