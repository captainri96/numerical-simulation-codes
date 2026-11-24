import numpy as np
import pandas as pd
import csv

patterns = ['Monocrop', 'Rows_Columns', 'Diagonal',\
            'Row strips', 'Column strips', 'Patches']

column_name =['Mono', 'Row','Diagonal', 'Row Strips', 'Column Strips','Patches']

##row_name = ['\u03BB=1, \u03C3=2.5', '\u03BB=1, \u03C3=4', \
##            '\u03BB=2, \u03C3=2.5', '\u03BB=2, \u03C3=4', \
##            '\u03BB=5, \u03C3=2.5', '\u03BB=2, \u03C3=4']

row_name = ['lambda=1, sigma=2.5', 'lambda=1, sigma=4', \
            'lambda=2, sigma=2.5', 'lambda=2, sigma=4', \
            'lambda=5, sigma=2.5', 'lambda=5, sigma=4']


sig = [2.5, 4] #insect mobility: # 1.0, 2.5, 4.0 -> poor mobility
lambd = [1, 2, 5]   #trap strength: 1.0, 2.0, 5 +inf  -> perfect trap strength
N, realization = 1000, 100

df = pd.read_csv(r'Trap_crops_20_by_50_field.csv')
trap_ = df.to_numpy()
traps = trap_[:,1:]

df_init = pd.read_csv(r'Nodes for the 100 random realizations.csv')
initial_nodes = df_init.to_numpy()
realizations = initial_nodes[:,1:]


#### SAMPLES

for lambdA in lambd:
    for sigma in sig:

        v_field = np.zeros((100,6), dtype='f')
  
        for realizatiOn in range(realization):
        
            for pattern in range(6):
                
                initial_infected_node = realizations[realizatiOn,pattern]
                pattern_name = patterns[pattern] 

                df1 = pd.read_csv(f"({realizatiOn})_remov_{pattern_name}_{initial_infected_node}_sigma={sigma}_lambda={lambdA}.csv")
                df2 = pd.read_csv(f"Equilibrium_time_realization_{realizatiOn}_sigma={sigma}_lambda={lambdA}.csv")
                
                rho_i, t_e = df1.to_numpy(), df2.to_numpy()
                rho_i, t_e = rho_i[:,1:], t_e[:,1:]

                print(f'\nIntercropping pattern: realization={realizatiOn}_ sigma={sigma},lambda={lambdA}')

                if pattern == 0: count = 1000
                else: count = 500

                sum_wi_vi = 0
                sum_rho_i = 0 #np.sum(rho_i[:,pattern], axis=0)

                for k in range(N):
                    if traps[k,pattern] != np.inf:
                        E = int(t_e[k,pattern])
                        sum_rho_i += rho_i[k, E-1]
                
                
                for node in range(N):
                    if traps[node,pattern] != np.inf:
                        E = int(t_e[node,pattern])
                        wi = rho_i[node, E-1] / sum_rho_i
                        vi = rho_i[node, E-1] / t_e[node, pattern]

                        sum_wi_vi += (wi*vi)

                v_field[realizatiOn, pattern] = float(count * sum_wi_vi) #count is the total number of crops

        v_fields = pd.DataFrame(v_field)
        v_fields.columns = column_name
        #v_fields.index = row_name

        v_fields.to_csv(f"Mean Infection Rate_vfields_realization_sigma={sigma}_lambda={lambdA}.csv")
        
##        row+=1
##
##                
##R_ave = pd.DataFrame(r_ave)
##R_ave.columns = column_name
##R_ave.index = row_name
##
##R_ave.to_csv(f"Mean Percentage of Removed Plants.csv")


###SAMPLE MEAN
        
##mean_v_field, row = np.zeros((6,6), dtype='f'), 0




###### SAMPLE STANDARD DEV
##
##stdev, row = np.zeros((6,6), dtype='f'), 0
##
##for lambdA in lambd:
##    for sigma in sig:
##
##        df2 = pd.read_csv(f"Mean Percentage of Removed Plants.csv")
##        
##        xi_mean = df2.to_numpy()
##        xi_mean = xi_mean[:,1:]
##        
##        for pattern in range(6):
##            xi_xmean = 0
##            print(f'\nIntercropping pattern: {pattern_name}_ sigma={sigma},lambda={lambdA}')
##            
##            for k in range(realizations):
##                pattern_name = patterns[pattern] 
##
##                xi_xmean += (r_i[k, pattern] - xi_mean[row,pattern])**2
##                
##                
##            stdev[row,pattern] = float(xi_xmean/(realizations-1))
##
##        row+=1
##                
##stDev = pd.DataFrame(stdev)
##stDev.columns = column_name
##stDev.index = row_name
##
##stDev.to_csv(f"Mean Percentage of Removed Plants_(STDEV output values).csv")
##
##
###### CONFIDENCE INTERVALS (CI)
##
##margin, row = np.zeros((6,6), dtype='f'), 0
##t_critical = 1.984
##
##for lambdA in lambd:
##    for sigma in sig:
##
##        df3 = pd.read_csv(f"Mean Percentage of Removed Plants_(STDEV output values).csv")
##        
##        stdv = df3.to_numpy()
##        stdv = stdv[:,1:]
##        
##        for pattern in range(6):
##            pattern_name = patterns[pattern] 
##            print(f'\nIntercropping pattern: {pattern_name}_ sigma={sigma},lambda={lambdA}')
##
##            margin[row,pattern] = t_critical * (stdv[row,pattern] / 10) #(stdv[k,pattern] / np.sqrt(realizations)
##
##        row+=1
##                
##confid = pd.DataFrame(margin)
##confid.columns = column_name
##confid.index = row_name
##
##confid.to_csv(f"Mean Percentage of Removed Plants_(Margin_of_Errors_CI).csv")
##
##
##print('\nDone!\n')
