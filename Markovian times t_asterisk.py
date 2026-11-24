import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp


df = pd.read_csv(r'Trap_crops_20_by_50_field.csv')
traps = df.to_numpy()
trap_crop = traps[:,1:]

patterns = ['Monocrop', 'Rows_Columns', 'Diagonal',\
            'Row strips', 'Column strips', 'Patches']

markovian_t = np.full((1000,6), 100, dtype = 'f')
column_name =['Mono', 'Ro_Cols','Diag', 'RowStps', 'ColStps','Pat']

sig = [2.5, 4] #insect mobility: # 1.0, 2.5, 4.0 -> poor mobility
lambd = [1, 2, 5]  #trap strength: 1.0, 2.0, 5 +inf  -> perfect trap strength
#sig, lambd = [2.5, 4], [10]

m, n, N, t = 19, 98, 1000, 100

df = pd.read_csv(r'Nodes for the 100 random realizations.csv')
bounds = df.to_numpy()
bound = bounds[:,1:]

for sigma in sig:
    for lambdA in lambd:
        print(f'Markovian time-t, sigma={sigma}, lambda={lambdA}\n')
        for k in range(6):
            # Define the path to the CSV file
            each = patterns[k]
            #csv_file_path1 = f'(Average)_sus_{patterns[k]}_sigma={sigma}_lambda={lambdA}.csv'
            #csv_file_path2 = f'(Average)_remov_{patterns[k]}_sigma={sigma}_lambda={lambdA}.csv'

            csv_file_path1 = f'(0)_sus_{each}_0_sigma={sigma}_lambda={lambdA}.csv'
            csv_file_path2 = f'(0)_remov_{each}_0_sigma={sigma}_lambda={lambdA}.csv'

            # Read the CSV file into a Pandas DataFrame
            df1 = pd.read_csv(csv_file_path1)
            df2 = pd.read_csv(csv_file_path2)

            # Convert the DataFrame to a NumPy array
            sus, remo    = df1.to_numpy(), df2.to_numpy()        #dimensions = sus.shape
            sus, remo = sus[:,1:], remo[:,1:]                    #rows, cols = dimensions

            for x in range(N):
                if trap_crop[x,k] == np.inf:
                    markovian_t[x,k] = np.inf #converts node value to 'inf' if it's a trap plant
                else:
                    for y in range(1,t):
                        if remo[x,y] > sus[x,y]:
                            markovian_t[x,k] = y #that is, y = y-1+(1) since to plot the days with equiv. colors, we must start at t=1, instead of t=0
                            break
                        
                        if y==99 and (remo[x,y] < sus[x,y]):
                            markovian_t[x,k] = 100  #t=99th+1 = 100
                
        Markov = pd.DataFrame(markovian_t, columns = column_name)
        #Markov.to_csv(f'Markovian time-t, sigma={sigma}, lambda={lambdA}.csv')
        Markov.to_csv(f'_Markovian time-t, sigma={sigma}, lambda={lambdA}.csv')


