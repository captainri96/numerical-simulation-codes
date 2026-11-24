import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import os

"""MAIN"""

print("\nHere is a list of the different cropping arrangements:\n")
distn = {0:'Monocrop', 1:'Rows_Columns', 2:'Diagonal',\
         3:'Row strips', 4:'Column strips', 5:'Patches'}
print(distn)

sig = [2.5, 4] #insect mobility: # 1.0, 2.5, 4.0 -> poor mobility
lambd = [1, 2, 5]  #trap strength: 1.0, 2.0, 5 +inf  -> perfect trap strength


m, n, N, t, realization = 19, 98, 1000, 100, 100

s_mean, e_mean = np.zeros((N,t), dtype='f'), np.zeros((N,t), dtype='f')
p_mean, z_mean = np.zeros((N,t), dtype='f'), np.zeros((N,t), dtype='f')

df = pd.read_csv(r'Nodes for the 100 random realizations.csv')
bounds = df.to_numpy()
bound = bounds[:,1:]

for pattern in range(6):
    if pattern == 0 : count = 1000
    else: count = 500
    
    for sigma in sig:
        for lambdA in lambd:
            pattern_name = distn[pattern] #print(f'\nRealization: {realizatiOn}')
            print(f'\nIntercropping pattern: {pattern_name}_ sigma={sigma},lambda={lambdA}')
            
            s_ave, e_ave = np.zeros((realization,N,t), dtype='f'), np.zeros((realization,N,t), dtype='f')
            p_ave, z_ave = np.zeros((realization,N,t), dtype='f'), np.zeros((realization,N,t), dtype='f')
            #creates a 3-dimensional array with np.zeros((frames, rows, columns))
            
            for realizatiOn in range(100):
                initial_infected_node = bound[realizatiOn,pattern]
                
                df1 = pd.read_csv(f"({realizatiOn})_sus_{pattern_name}_{initial_infected_node}_sigma={sigma}_lambda={lambdA}.csv")
                df2 = pd.read_csv(f"({realizatiOn})_expo_{pattern_name}_{initial_infected_node}_sigma={sigma}_lambda={lambdA}.csv")
                df3 = pd.read_csv(f"({realizatiOn})_infec_{pattern_name}_{initial_infected_node}_sigma={sigma}_lambda={lambdA}.csv")
                df4 = pd.read_csv(f"({realizatiOn})_remov_{pattern_name}_{initial_infected_node}_sigma={sigma}_lambda={lambdA}.csv")

                s_av, e_av, p_av, z_av = df1.to_numpy(), df2.to_numpy(), df3.to_numpy(), df4.to_numpy()

                s_ave[realizatiOn,:,:], e_ave[realizatiOn,:,:] = s_av[:,1:], e_av[:,1:]
                p_ave[realizatiOn,:,:], z_ave[realizatiOn,:,:] = p_av[:,1:], z_av[:,1:]

            for crop in range(N):
                for time in range(t):
                    all_s, all_e = np.array([], dtype='f'), np.array([], dtype='f') 
                    all_p, all_z = np.array([], dtype='f'), np.array([], dtype='f')
                    
                    for each_realization in range(realization):
                        all_s = np.append(all_s, s_ave[each_realization,crop,time])
                        all_e = np.append(all_e, e_ave[each_realization,crop,time])
                        all_p = np.append(all_p, p_ave[each_realization,crop,time])
                        all_z = np.append(all_z, z_ave[each_realization,crop,time])

                    s_mean[crop,time], e_mean[crop,time] = np.sum(all_s)/count, np.sum(all_e)/count
                    p_mean[crop,time], z_mean[crop,time] = np.sum(all_p)/count, np.sum(all_z)/count
                           
            S, E, P, Z = pd.DataFrame(s_mean), pd.DataFrame(e_mean), pd.DataFrame(p_mean), pd.DataFrame(z_mean)

            S.to_csv(f"_(Average)_sus_{pattern_name}_sigma={sigma}_lambda={lambdA}.csv")
            E.to_csv(f"_(Average)_expo_{pattern_name}_sigma={sigma}_lambda={lambdA}.csv")
            P.to_csv(f"_(Average)_infec_{pattern_name}_sigma={sigma}_lambda={lambdA}.csv")
            Z.to_csv(f"_(Average)_remov_{pattern_name}_sigma={sigma}_lambda={lambdA}.csv")

print('\nDone!\n')
