import numpy as np
import pandas as pd
import csv

patterns = ['Monocrop', 'Rows', 'Diagonal',\
            'Row strips', 'Column strips', 'Patches']

column_name =['Mono', 'Row','Diagonal', 'Row Strips', 'Column Strips','Patches']
row_name = ['\u03BB=1, \u03C3=2.5', '\u03BB=1, \u03C3=4', \
            '\u03BB=2, \u03C3=2.5', '\u03BB=2, \u03C3=4', \
            '\u03BB=5, \u03C3=2.5', '\u03BB=2, \u03C3=4']

row_name = ['lambda=1, sigma=2.5', 'lambda=1, sigma=4', \
            'lambda=2, sigma=2.5', 'lambda=2, sigma=4', \
            'lambda=5, sigma=2.5', 'lambda=5, sigma=4']


sig = [2.5, 4] #insect mobility: # 1.0, 2.5, 4.0 -> poor mobility
lambd = [1, 2, 5]   #trap strength: 1.0, 2.0, 5 +inf  -> perfect trap strength
N, realizations = 1000, 100


#### SAMPLE MEAN
r_ave, row = np.zeros((6,6), dtype='f'), 0

for lambdA in lambd:
    for sigma in sig:

        df1 = pd.read_csv(f"Proportion of Removed per Realization_sigma={sigma}_lambda={lambdA}.csv")
        
        r_i = df1.to_numpy()
        r_i = r_i[:,1:]
        
        for pattern in range(6):
            pattern_name = patterns[pattern] 
            print(f'\nIntercropping pattern: {pattern_name}_ sigma={sigma},lambda={lambdA}')

            r_ave[row,pattern] = np.mean(r_i[:, pattern], axis=0)

        row+=1
                
R_ave = pd.DataFrame(r_ave)
R_ave.columns = column_name
R_ave.index = row_name

R_ave.to_csv(f"Mean Percentage of Removed Plants.csv")




#### SAMPLE STANDARD DEV

stdev, row = np.zeros((6,6), dtype='f'), 0

for lambdA in lambd:
    for sigma in sig:

        df2 = pd.read_csv(f"Mean Percentage of Removed Plants.csv")
        
        xi_mean = df2.to_numpy()
        xi_mean = xi_mean[:,1:]
        
        for pattern in range(6):
            xi_xmean = 0
            print(f'\nIntercropping pattern: {pattern_name}_ sigma={sigma},lambda={lambdA}')
            
            for k in range(realizations):
                pattern_name = patterns[pattern] 

                xi_xmean += (r_i[k, pattern] - xi_mean[row,pattern])**2
                
                
            stdev[row,pattern] = float(xi_xmean/(realizations-1))

        row+=1
                
stDev = pd.DataFrame(stdev)
stDev.columns = column_name
stDev.index = row_name

stDev.to_csv(f"Mean Percentage of Removed Plants_(STDEV output values).csv")


#### CONFIDENCE INTERVALS (CI)

margin, row = np.zeros((6,6), dtype='f'), 0
t_critical = 1.984

for lambdA in lambd:
    for sigma in sig:

        df3 = pd.read_csv(f"Mean Percentage of Removed Plants_(STDEV output values).csv")
        
        stdv = df3.to_numpy()
        stdv = stdv[:,1:]
        
        for pattern in range(6):
            pattern_name = patterns[pattern] 
            print(f'\nIntercropping pattern: {pattern_name}_ sigma={sigma},lambda={lambdA}')

            margin[row,pattern] = t_critical * (stdv[row,pattern] / 10) #(stdv[k,pattern] / np.sqrt(realizations)

        row+=1
                
confid = pd.DataFrame(margin)
confid.columns = column_name
confid.index = row_name

confid.to_csv(f"Mean Percentage of Removed Plants_(Margin_of_Errors_CI).csv")


print('\nDone!\n')
