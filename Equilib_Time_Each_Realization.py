import numpy as np
import pandas as pd
import csv

patterns = ['Monocrop', 'Rows_Columns', 'Diagonal',\
            'Row strips', 'Column strips', 'Patches']
column_name =['Mono', 'Ro_Cols','Diag', 'RowStps', 'ColStps','Pat']

sig = [2.5, 4] #insect mobility: # 1.0, 2.5, 4.0 -> poor mobility
lambd = [1, 2, 5]   #trap strength: 1.0, 2.0, 5 +inf  -> perfect trap strength

N, tot_time, err = 1000, 100, 1e-3 #0.001  #the higher the error, the earlier the equilibrium time becomes; also very sensitive to small changes in err

m, n, N, t, realization = 19, 98, 1000, 100, 100

df = pd.read_csv(r'Trap_crops_20_by_50_field.csv')
trap_ = df.to_numpy()
traps = trap_[:,1:]


for sigma in sig:
    for lambdA in lambd:
        equilib = np.full((N,6), np.inf)
        for k in range(6):
            # Read the CSV file into a Pandas DataFrame
            df1 = pd.read_csv(f'(Average)_sus_{patterns[k]}_sigma={sigma}_lambda={lambdA}.csv')
            df2 = pd.read_csv(f'(Average)_expo_{patterns[k]}_sigma={sigma}_lambda={lambdA}.csv')
            df3 = pd.read_csv(f'(Average)_infec_{patterns[k]}_sigma={sigma}_lambda={lambdA}.csv')
            df4 = pd.read_csv(f'(Average)_remov_{patterns[k]}_sigma={sigma}_lambda={lambdA}.csv')

            # Convert the DataFrame to a NumPy array
            sus, expo, infec, remo    = df1.to_numpy(), df2.to_numpy(), df3.to_numpy(), df4.to_numpy()
            sus, expo, infec, remo = sus[:,1:], expo[:,1:], infec[:,1:], remo[:,1:]

##            for u in range(N):
##                for v in range(tot_time):
##                    if sus[u,v]<0: sus[u,v] = 0
##                    if expo[u,v]<0: expo[u,v] = 0
##                    if infec[u,v]<0: infec[u,v] = 0
##                    if remo[u,v]<0: remo[u,v] = 0        
            #equilib_time_T = 0
            
            print(f'\nPattern: {patterns[k]}, sigma={sigma}, lambda={lambdA}')
            for node in range(N):
                if traps[node,k] != np.inf:
                    for time in range(1,tot_time):
                        
                        if time == 99:
                            equilib[node,k] = 100

                        d_T = 0.5*( abs(sus[node,time]  - sus[node,time-1]) + \
                                    abs(expo[node,time] - expo[node,time-1]) + \
                                    abs(infec[node,time] - infec[node,time-1]) + \
                                    abs(remo[node,time] - remo[node,time-1])      )
                        
                        if d_T < err:
                            equilib[node,k] = time
                            break
                        
                        
##                        if ((abs(sus[node,time+1] - sus[node,time]) < err) and \
##                           (abs(expo[node,time+1] - expo[node,time]) < err) and \
##                           (abs(infec[node,time+1] - infec[node,time]) < err) and \
##                           (abs(remo[node,time+1] - remo[node,time]) < err)):

                            #equilib_time_T = time
##                            equilib[node,k] = time
                        
##                            print(f'\nsus[{node+1},{time+1}] - sus[{node+1},{time}]: {abs(sus[node,time+1] - sus[node,time])}')
##                            print(f'expo[{node+1},{time+1}] - expo[{node+1},{time}]: {abs(expo[node,time+1] - expo[node,time])}')
##                            print(f'infec[{node+1},{time+1}] - infec[{node+1},{time}]: {abs(infec[node,time+1] - infec[node,time])}')
##                            print(f'remo[{node+1},{time+1}] - remo[{node+1},{time}]: {abs(remo[node,time+1] - remo[node,time])}\n')
##                            break
                            
                             
                            #print(f'At node {node} -> equilib. time T: {equilib_time_T}')
            #print(f'\nEquilibrium time T for the {patterns[k]} \n arrangement when \u03C3={sigma}, \u03BB={lambdA}: {equilib_time_T}\n')
            #equilib[1000,k] = np.max(equilib[:,k])
            #print(f'\nEquilibrium time T for the {patterns[k]} \n arrangement when \u03C3={sigma}, \u03BB={lambdA}: {equilib[1000,k]}')            

        equilibrium = pd.DataFrame(equilib, columns = column_name)
        equilibrium.to_csv(f"Equilibrium time T_sigma={sigma}_lambda={lambdA}.csv")
                
                
