import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd

print("\nHere is a list of the different cropping arrangements:\n")
distn = {0:'Monocrop', 1:'Rows_Columns', 2:'Diagonal',\
         3:'Row strips', 4:'Column strips', 5:'Patches'}

patterns =['Monocrop', 'Row','Diagonal', 'Row Strips', 'Column Strips','Patches']

sig = [2.5, 4] #insect mobility: # 1.0, 2.5, 4.0 -> poor mobility
lambd = [1, 2, 5]   #trap strength: 1.0, 2.0, 5 +inf  -> perfect trap strength

m, n, N, tot_time, realization, err = 19, 98, 1000, 100, 100, 1e-3 #0.001

df = pd.read_csv(r'Trap_crops_20_by_50_field.csv')
trap_ = df.to_numpy()
traps = trap_[:,1:]

df_init = pd.read_csv(r'Nodes for the 100 random realizations.csv')
initial_nodes = df_init.to_numpy()
realizations = initial_nodes[:,1:]


for sigma in sig:
    for lambdA in lambd:
    
        xi_mean = np.zeros((realization,len(patterns)), dtype='f')

        for realizatiOn in range(100):
            for pattern in range(6):
                
                pattern_name = distn[pattern]
                
                print(f'\nIntercropping pattern: realization: {realizatiOn}, {pattern_name}_ sigma={sigma},lambda={lambdA}')

                initial_infected_node = realizations[realizatiOn,pattern]
                
                df1 = pd.read_csv(f"({realizatiOn})_sus_{pattern_name}_{initial_infected_node}_sigma={sigma}_lambda={lambdA}.csv")
                df2 = pd.read_csv(f"({realizatiOn})_expo_{pattern_name}_{initial_infected_node}_sigma={sigma}_lambda={lambdA}.csv")
                df3 = pd.read_csv(f"({realizatiOn})_infec_{pattern_name}_{initial_infected_node}_sigma={sigma}_lambda={lambdA}.csv")
                df4 = pd.read_csv(f"({realizatiOn})_remov_{pattern_name}_{initial_infected_node}_sigma={sigma}_lambda={lambdA}.csv")

                sus, expo, infec, remo    = df1.to_numpy(), df2.to_numpy(), df3.to_numpy(), df4.to_numpy()
                sus, expo, infec, remo = sus[:,1:], expo[:,1:], infec[:,1:], remo[:,1:]

                if pattern == 0: w = N
                else: w = 500
                 
                rho_i_equilib, count = np.full((w,1), np.inf), 0
                
                for node in range(N):
                    if traps[node,pattern] != np.inf:
                        for time in range(1,tot_time):
                            if time == 99:
                                equilib_time = 100
                                rho_i_equilib[count,0] = remo[node, equilib_time-1]

                            d_T = 0.5*( abs(sus[node,time]  - sus[node,time-1]) + \
                                        abs(expo[node,time] - expo[node,time-1]) + \
                                        abs(infec[node,time] - infec[node,time-1]) + \
                                        abs(remo[node,time] - remo[node,time-1])      )
                            
                            if d_T < err:
                                equilib_time = time
                                rho_i_equilib[count,0] = remo[node, equilib_time]
                                break    
                        
                        count+=1

                #Get the mean for all rho_i's at each equilibrium time

                xi_mean[realizatiOn,pattern] = np.mean(rho_i_equilib[:,0])


        xi_means = pd.DataFrame(xi_mean, columns = patterns)
        xi_means.to_csv(f"Proportion of Removed per Realization_sigma={sigma}_lambda={lambdA}.csv")

print('\n\nDone!')
                                
                        




