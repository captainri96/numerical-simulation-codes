import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.integrate import odeint
from scipy.integrate import solve_ivp

pattern = ['Monocrop', 'Rows_Columns', 'Diagonal',\
            'Row strips', 'Column strips', 'Patches']

sig = [2.5, 4] #insect mobility: # 1.0, 2.5, 4.0 -> poor mobility
lambd = [1, 2, 5]  #trap strength: 1.0, 2.0, 5 +inf  -> perfect trap strength

df = pd.read_csv(r'Trap_crops_20_by_50_field.csv')
trap_ = df.to_numpy()
traps = trap_[:,1:]
N = 1000

print('\nIntercropping patterns:\n', pattern)
print(f'Values for sigma, \u03C3: {sig} and lambda, \u03BB: {lambd}')

k = int(input('\nChoose intercropping arrangement (0-5): '))
qq = input('Is \u03C3 a float value? y or n? ')
if qq == 'y':
    sigma = float(input('Enter value of \u03C3: '))
else:
    sigma = int(input('Enter value of \u03C3: '))
lambdA = int(input('Enter value of \u03BB: '))


print('\n')
##for sigma in sig:
##    for lambdA in lambd:
##        for k in range(6):

#init_bound = int(input('\nEnter  node initially infected (0-999): '))

# Define the path to the CSV file
csv_file_path1 = f'(0)_sus_{pattern[k]}_0_sigma={sigma}_lambda={lambdA}.csv'
csv_file_path2 = f'(0)_expo_{pattern[k]}_0_sigma={sigma}_lambda={lambdA}.csv'
csv_file_path3 = f'(0)_infec_{pattern[k]}_0_sigma={sigma}_lambda={lambdA}.csv'
csv_file_path4 = f'(0)_remov_{pattern[k]}_0_sigma={sigma}_lambda={lambdA}.csv'

# Read the CSV file into a Pandas DataFrame
df1 = pd.read_csv(csv_file_path1)
df2 = pd.read_csv(csv_file_path2)
df3 = pd.read_csv(csv_file_path3)
df4 = pd.read_csv(csv_file_path4)

# Convert the DataFrame to a NumPy array
sus    = df1.to_numpy()
expos  = df2.to_numpy()
infec  = df3.to_numpy()
remo   = df4.to_numpy()

#sus, expos, infec, remo = sus[:,1:], expos[:,1:], infec[:,1:], remo[:,1:]

# Print the DataFrame and the NumPy array
##print("Pandas DataFrame:")
##print(df)
##print("\nNumPy Array:")
##print(data_array)


t = np.linspace(0,99,100)
#plant = int(input('Enter crop number/position: '))+1
#for plant in range(len(sus)):
choose = 'y'
while(choose=='y'):
    #plant = int(input('Choose crop number (1-1000): '))
    for plant in range(1,N+1):
        if traps[plant,k] != np.inf:
            s = sus[plant-1,1:]
            e = expos[plant-1,1:]
            p = infec[plant-1,1:]
            z = remo[plant-1,1:]

            plt.plot(t, s, label = 'susceptible')
            plt.plot(t, e, label = 'exposed')
            plt.plot(t, p, label = 'infected')
            plt.plot(t, z, label = 'removed')
            plt.legend()
            plt.xlabel("time")
            plt.title(f'crop {plant} ({pattern[k]}, \u03C3={sigma}, \u03BB={lambdA})')
            plt.show()

    choose = input('Choose another crop? y or n? ')

