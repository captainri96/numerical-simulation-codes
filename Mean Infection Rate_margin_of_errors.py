import numpy as np
import pandas as pd
import csv

patterns = ['Monocrop', 'Rows', 'Diagonal',\
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


#### SAMPLES

row = 0
means_vfields = np.zeros((6,6), dtype='f')
margin_errors = np.zeros((6,6), dtype='f')


for lambdA in lambd:
    for sigma in sig:

        df = pd.read_csv(fr'Mean Infection Rate_vfields_realization_sigma={sigma}_lambda={lambdA}.csv') #_sigma={sigma}_lambda={lambdA}
        xi_vfield = df.to_numpy()
        xi_vfield = xi_vfield[:,1:]
  
        for realizatiOn in range(realization):

            for pattern in range(6):
                
                pattern_name = patterns[pattern] 

                print(f'\nIntercropping pattern: pattern={patterns[pattern]}_ sigma={sigma},lambda={lambdA}')

                realization_mean = np.mean(xi_vfield[:,pattern])
                realization_stdev = np.std(xi_vfield[:,pattern])
                margin_of_error = 1.984 * realization_stdev/10

                means_vfields[row,pattern] = realization_mean
                margin_errors[row,pattern] = margin_of_error

        row += 1

mean_v_fields = pd.DataFrame(means_vfields, columns = column_name, index = row_name)
mean_v_fields.to_csv(f"Mean Infection Rate_vfields_ALL_realizations.csv")

margin_error = pd.DataFrame(margin_errors, columns = column_name, index = row_name)
margin_error.to_csv(f"Mean Infection Rate_Margin_of_Errors.csv")


        
