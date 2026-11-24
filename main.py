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


k1, k2P, k3P, theta, mu = 2, 0.2, 0.08, 1, 0.00105
T = float(0.5/theta)
phi = 1 - np.exp(-k1*T)
k2 = 1-np.exp(-k2P)
k3 = 1-np.exp(-k3P)

sig = [2.5, 4] #insect mobility: # 1.0, 2.5, 4.0 -> poor mobility
lambd = [1, 2, 5]  #trap strength: 1.0, 2.0, 5 +inf  -> perfect trap strength
#sig, lambd = [2.5, 4], [10]

m, n, N, t = 19, 98, 1000, 100

df1 = pd.read_csv(r'Trap_crops_20_by_50_field.csv')
trap_ = df1.to_numpy()
traps = trap_[:,1:]

df2 = pd.read_csv(r'Nodes for the 100 random realizations.csv')
bounds = df2.to_numpy()
bound = bounds[:,1:]

for realizatiOn in range(100): #range(99,49, -1)
    for sigma in sig:
        for lambdA in lambd:
            for pattern in range(6):
                title = distn[pattern]
                print(f'\n{pattern+1}. Intercropping pattern: {title}')
                print(f'Realization: {realizatiOn}_ sigma={sigma},lambda={lambdA},{distn[pattern]}')
                
                df = pd.read_csv(f'A_tilde_ sigma={sigma},lambda={lambdA},{distn[pattern]}.csv')
                a_Tilde = df.to_numpy()
                aij_Tilde = a_Tilde[:,1:]

                s, e = np.zeros((N,t), dtype='f'), np.zeros((N,t), dtype='f')
                p, z = np.zeros((N,t), dtype='f'), np.zeros((N,t), dtype='f')

                initial_infected_node = bound[realizatiOn,pattern]
                

                for i in range(N): ####should be for i in "range(N)" not (1,N)
                    #if node i is a trap crop
                    if traps[i,pattern] == np.inf:
                        z[i,0] = 1      #initial value: z_i(crop 2 to N,time 0) => z_i(i,0)
                        #s[i,0], e[i,0], p[i,0] = 0, 0, 0
                    else:
                        s[i,0] = 1      #initial value: s_i(crop 2 to N,time 0) => s_i(i,0)
                        #e[i,0], p[i,0], z[i,0] = 0, 0, 0

                #Corresponds to the initially infected  node at time 0:
                p[initial_infected_node,0] = 1  #initial value: p_i(crop_i,time t) => p_i(0,0)
                s[initial_infected_node,0] = 0
                e[initial_infected_node,0] = 0
                z[initial_infected_node,0] = 0


                for time in range(0,t-1):
                    for crop_i in range(N):
                        #for each secondary crop
                        if traps[crop_i,pattern] == np.inf:
                            #print(f'crop: {crop_i+1} - trap crop')
                            s[crop_i, time+1] = 0
                            e[crop_i, time+1] = 0
                            p[crop_i, time+1] = 0
                            z[crop_i, time+1] = 1

                        #for each crop in the main cultivar
                        else:
                            product = 1
                            for j in range(N):
                                product = product*(1-(phi*aij_Tilde[crop_i,j]*p[j,time]))
                            q = 1-product

                            e[crop_i,time+1] = e[crop_i,time]*(1-mu) - k2*e[crop_i,time] + s[crop_i,time]*q
                            p[crop_i,time+1] = k2*e[crop_i,time] + p[crop_i,time]*(1-mu) - k3*p[crop_i,time]
                            z[crop_i,time+1] = k3*p[crop_i,time] + z[crop_i,time]*(1-mu) + mu
                            s[crop_i,time+1] = 1 - e[crop_i,time+1] - p[crop_i,time+1] - z[crop_i,time+1]


                S = pd.DataFrame(s)
                E = pd.DataFrame(e)
                P = pd.DataFrame(p)
                Z = pd.DataFrame(z)

                S.to_csv(f"({realizatiOn})_sus_{title}_{initial_infected_node}_sigma={sigma}_lambda={lambdA}.csv")
                E.to_csv(f"({realizatiOn})_expo_{title}_{initial_infected_node}_sigma={sigma}_lambda={lambdA}.csv")
                P.to_csv(f"({realizatiOn})_infec_{title}_{initial_infected_node}_sigma={sigma}_lambda={lambdA}.csv")
                Z.to_csv(f"({realizatiOn})_remov_{title}_{initial_infected_node}_sigma={sigma}_lambda={lambdA}.csv")

##FIND saved CSV files
##current_directory = os.getcwd()
