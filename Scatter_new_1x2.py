import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.figure import Figure
import matplotlib.cm as cm
import matplotlib.patches as mpatches
import matplotlib.font_manager as font_manager

#csV = int(input("Enter 0 for initial node 0 and 1 if you opt to choose 'ave' files: "))

distn = {0:'Monocrop', 1:'Rows/Columns', 2:'Diagonal',\
         3:'Row strips', 4:'Column strips', 5:'Patches'}

column_name =['Mono', 'Ro_Cols','Diag', 'RowStps', 'ColStps','Pat']

labels = {0:'Monocrop', 1:'Row', 2:'Diagonal',\
         3:'Row Strips', 4:'Column Strips', 5:'Patches'}

sig = [2.5, 4] #insect mobility: # 1.0, 2.5, 4.0 -> poor mobility
lambd = [1, 2, 5]   #trap strength: 1.0, 2.0, 5 +inf  -> perfect trap strength
##lambd = [1] 
N, t, n = 1000, 100, 500

df_A = pd.read_csv(r'A_ij.csv')
Aij = df_A.to_numpy()
Aij = Aij[0,1:] #print('Shortest distances (from initial node of infection to node i):\n', Aij)

for sET in range(3):
    seT_pattern = 1
    if sET == 0: a, b = 0, 2
    elif sET == 1: a, b = 2, 4
    else: a, b = 4, 6
    
    # Generating multiple datasets
    for lambdA in lambd:
        
        # Read the CSV file into a Pandas DataFrame
        df1 = pd.read_csv(f'(0) Proportion of Removed at Equilib t_sigma=2.5_lambda={lambdA}.csv')
        df2 = pd.read_csv(f'(0) Proportion of Removed at Equilib t_sigma=4_lambda={lambdA}.csv')

        # Convert the DataFrame to a NumPy array
        av_removed_25 = df1.to_numpy()
        av_removed_4 = df2.to_numpy()
        
        av_removed_25 = av_removed_25[:,1:]
        av_removed_4 = av_removed_4[:,1:]  

        fig, ax = plt.subplots(1, 2, figsize=(9, 3.5) )
        ind = [[0,0], [0,1]]

        for k in range(a, b):   #sets: (0,2), (2,4), (4,6)
            #u, v = ind[k][0], ind[k][1]  #ind[which sub-array][which of the two values]
            x_25, x_4, y_25, y_4 = [], [], [], []
            count1, count2 = 0, 0
            
            if k < 2: q, seT = k, 'A'
            elif k<4 and k>=2: q, seT = k-2, 'B'
            else: q, seT = k-4,  'C'

            for node in range(N):
                if av_removed_25[node,k] > 0:
                    y_25.append(av_removed_25[node,k])
                    x_25.append(Aij[node])
                else:
                    count1 += 1

                if av_removed_4[node,k] > 0:
                    y_4.append(av_removed_4[node,k])
                    x_4.append(Aij[node])
                else:
                    count2 += 1
            
            x = x_25 + x_4
            y = y_25 + y_4

            n1 = len(y_25) #or len(y_25)
            n2 = len(y_4) #or len(y_4)


            if lambdA == 1:
                location = "upper right" #"lower right"
                k1, k2 = 0.6, 0.9
                cmp = 'inferno'
            elif lambdA == 2:
                k1, k2 = 0.1, 0.5 #0.5, 0.98
                cmp = 'viridis'

                if k==0: location = 'center right'
                else: location = "best"
                
            else:
                k1, k2 = 0.3, 0.9
                cmp = 'inferno'
                
                if k==0: location = 'center right'
                else: location = "best"
                
            # Normalize values to fit Viridis colormap
            norm = mcolors.Normalize(vmin=0, vmax=1)
            cmap = cm.get_cmap(cmp) #viridis #Spectral #inferno

            values = [k1]*n1 + [k2]*n2   #0,1 #0.5, 0.98 # 0.05, 0.98
            scatter = ax[q].scatter(x, y, c = values, s=3, cmap=cmap, norm=norm)
            
            #ok1 [0.6]*n1 + [0.9]*n2 of inferno is "orange vs yellow"
            #ok2 [0.5]*n1 + [0.98]*n2 of viridis is "yellow and bluish yellow green"
            #ok3 [0.3]*n1 + [0.9]*n2 of inferno is ~= to 0,1 of viridis "purple vs yellow"
            # [0.05]*n1 + [0.98]*n2 of viridis is "purple vs yellow"
            # [0]*n1 + [0.9]*n2  of viridis is "purple and bluish yellow green"

            font1 = {'family':'Times New Roman','color':'darkred','size':19}
            font2 = {'family':'Times New Roman','color':'#01153e','size':19} #5f0b3e
            font3 = {'family':'serif','color':'black'}
            font4 = font_manager.FontProperties(family='serif',
                                       style='normal', size=10)
            
            #setting font color of each subplot's title
##            if k == 0: use_font = font1
##            else: use_font = font2
            use_font = font2

            # Set y-axis range
            if lambdA==1: ax[q].set_ylim(0.950, 1)
            else: ax[q].set_ylim(0, 1)
            
            ax[q].set_title(labels[k], fontdict = use_font, fontweight='bold', style='italic') 
            
            ax[q].set_ylabel(r"probability $\varrho_j$", fontsize = 15, fontdict = font3 )
            ax[q].set_xlabel(r"distance $d_{{i_0},j}$", fontsize = 15, fontdict = font3)

            print(f'\nlambda={lambdA}, pattern: {distn[k]}')

            classes = ['\u03C3 $=$ 2.5','\u03C3 $=$ 4']
            legend1 = ax[q].legend(handles=scatter.legend_elements()[0],
                                loc=location, labels=classes, prop = font4) #title="Insect mobility"
            ax[q].add_artist(legend1)
            plt.tight_layout() #controls the margin of the overall figure

        if lambdA == 1: this_set = 1
        elif lambdA == 2: this_set = 2
        else: this_set = 3


        fig.subplots_adjust(wspace=0.32, hspace=0.3) #adjusts the distances between subplots in each figure
        fig.set_dpi(500.0)  # This controls display resolution

        #seT_pattern += 1
        fig.savefig(f'(set {this_set}{seT})_1x2_scatter_plot_lambda={lambdA}.png', dpi=500) 
        #plt.show()


