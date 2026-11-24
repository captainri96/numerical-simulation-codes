import numpy as np
import pandas as pd
import csv

patterns = ['Monocrop', 'Rows_Columns', 'Diagonal',\
            'Row strips', 'Column strips', 'Patches']
column_name =['Mono', 'Ro_Cols','Diag', 'RowStps', 'ColStps','Pat']

sig = [2.5, 4] #insect mobility: # 1.0, 2.5, 4.0 -> poor mobility
lambd = [1, 2, 5]   #trap strength: 1.0, 2.0, 5 +inf  -> perfect trap strength

m, n, N, t, realization = 19, 98, 1000, 100, 100

df = pd.read_csv(r'Trap_crops_20_by_50_field.csv')
trap_ = df.to_numpy()
traps = trap_[:,1:]

remov_proportion = np.zeros((N,6), dtype='f')

for sigma in sig:
    for lambdA in lambd:
        for k in range(6):
            # Read the CSV file into a Pandas DataFrame
            df1 = pd.read_csv(f'(0)_remov_{patterns[k]}_0_sigma={sigma}_lambda={lambdA}.csv')
            df2 = pd.read_csv(f'Equilibrium time T_sigma={sigma}_lambda={lambdA}.csv')

            # Convert the DataFrame to a NumPy array
            remo, equilib = df1.to_numpy(), df2.to_numpy()
            remo, equilib = remo[:,1:], equilib[:,1:]
                           
            print(f'\nPattern: {patterns[k]}, sigma={sigma}, lambda={lambdA}')
            for node in range(N):
                if traps[node,k] != np.inf:
                    t_equilib = int(equilib[node,k]-1)
                    remov_proportion[node,k] = remo[node,t_equilib]
                  
          
        removed = pd.DataFrame(remov_proportion, columns = column_name)
        removed.to_csv(f"(0) Proportion of Removed at Equilib t_sigma={sigma}_lambda={lambdA}.csv")
                
                
