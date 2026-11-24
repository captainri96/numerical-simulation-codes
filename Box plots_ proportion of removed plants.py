import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

patterns = ['Monocrop', 'Rows_Columns', 'Diagonal',\
            'Row strips', 'Column strips', 'Patches']
column_name =['Mono', 'Ro_Cols','Diag', 'RowStps', 'ColStps','Pat']

sig = [2.5, 4] #insect mobility: # 1.0, 2.5, 4.0 -> poor mobility
lambd = [1, 2, 5]   #trap strength: 1.0, 2.0, 5 +inf  -> perfect trap strength
m, n, N, t, realization = 19, 98, 1000, 100, 100


# Generating multiple datasets
for lambdA in lambd:
    mono, row, diag = np.zeros(2*N, dtype='f'), np.zeros(N, dtype='f'), np.zeros(N, dtype='f')
    rowstp, colstp, patch = np.zeros(N, dtype='f'), np.zeros(N, dtype='f'), np.zeros(N, dtype='f')              
    
    # Read the CSV file into a Pandas DataFrame
    df1 = pd.read_csv(f'(0) Proportion of Removed at Equilib t_sigma=2.5_lambda={lambdA}.csv')
    df2 = pd.read_csv(f'(0) Proportion of Removed at Equilib t_sigma=4_lambda={lambdA}.csv')


    # Convert the DataFrame to a NumPy array
    av_removed_25, av_removed_4 = df1.to_numpy(), df2.to_numpy()
    av_removed_25, av_removed_4 = av_removed_25[:,1:], av_removed_4[:,1:]
    av_remov = np.concatenate((av_removed_25, av_removed_4))
                   
    #print(f'\nPattern: {patterns[k]}, sigma={sigma}, lambda={lambdA}')
    for node in range(2*N):
        if node <= (N-1):
            mono[node], row[node], diag[node] = av_remov[node,0], av_remov[node,1], av_remov[node,2]
            rowstp[node], colstp[node], patch[node] = av_remov[node,3], av_remov[node,4], av_remov[node,5]
        else:
            mono[node] = av_remov[node,0]

    #for pattern in range(6):
    high_m, high = ['high' for i in range(N)], ['high' for i in range(500)]
    low_m, low = ['low' for i in range(N)], ['low' for i in range(500)]
    combi = high + low


    data = {
        'Group': ['monocrop']*2*N + ['row']*N + ['diagonal']*N
                    + ['row strips']*N + ['column strips']*N + ['patches']*N,
        'Value': np.concatenate((mono, row, diag, rowstp, colstp, patch)),
        'Mobility': high_m + low_m + combi*5

    }
    ##'Insect mobility': ['high (u"U+1D70E"=2.5)']*100
    df = pd.DataFrame(data)

    # Plots graph
    sns.boxplot(x='Group', y='Value', data=df, hue='Mobility',
                     palette='Set2', width=0.7, dodge=True, gap=.1) #palette = 'Spectral', flare


    plt.title(f'Colored Boxplot (lambda={lambdA})')
    plt.show()

































### Generate multiple datasets
##data = {
##    'Group': ['A']*100 + ['B']*100 + ['C']*100,
##    'Value': np.concatenate([np.random.normal(0, 1, 100), 
##                             np.random.normal(1, 2, 100), 
##                             np.random.normal(2, 1.5, 100)])
##}
##df = pd.DataFrame(data)
### Create additional grouping data
##df['Subgroup'] = np.random.choice(['X', 'Y'], size=300)
### Plots graph
##sns.boxplot(x='Group', y='Value', data=df, hue='Subgroup', palette='Set2')
##plt.title('Colored Boxplot')
##plt.show()







