import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.figure import Figure
from matplotlib.patches import Circle


distn = {0:'Monocrop', 1:'Rows/Columns', 2:'Diagonal',\
         3:'Row strips', 4:'Column strips', 5:'Patches'}

labels = {0:'monocrop', 1:'row', 2:'diagonal',\
         3:'row strips', 4:'column strips', 5:'patches'}

# Step 1: Create a hexagonal grid of circle centers
rows = 20  # Number of rows of circles
cols = 50  # Number of columns of circles
radius = 0.8  # Radius of each circle
h_spacing = 2 * radius +0.2 # Horizontal spacing between circle centers
v_spacing = 2 * radius +0.2 # Vertical spacing between circle centers

# Create a grid of circle centers
circle_centers = []
for row in range(rows):
    for col in range(cols):
        # Alternating rows are shifted horizontally by half a circle's width
        x_shift = radius if row % 2 == 1 else 0
        x = col * h_spacing + x_shift
        y = row * v_spacing
        circle_centers.append((x, y))

# Step 2: Generate random data values for coloring the circles

sigma = [2.5, 4] #sig = int(input('\nEnter value of sigma: '))   
lambdA = [1, 2, 5] #lambd = int(input('\nEnter value of lambda: '))


print('\n')
for sig in sigma:
    for lambd in lambdA:
        df = pd.read_csv(f"(0)_Markovian time-t, sigma={sig}, lambda={lambd}.csv")
        markov_ = df.to_numpy()
        markov_t = markov_[:,1:]

        fig, ax = plt.subplots(3, 2, figsize=(9, 5.8)) 
        ind = [[0,0], [1,0], [2,0],[0,1], [1,1], [2,1]]
        
        for h in range(6): #loop for all arrangements
            data_values = markov_t[:,h]
            
            # Step 3: Create a colormap
            cmap = plt.get_cmap('RdYlGn') # turbo_r#Spectral #rainbow_r #gist_rainbow #jet_r #hsv #gist_rainbow
            #norm = mcolors.LogNorm(vmin=1, vmax=100) #vmin=Z.min(), vmax=Z.max()
            norm = mcolors.Normalize(vmin=1, vmax=100)  # Normalize data values to colormap range

            # Step 4: Plot the circles        
            u, v = ind[h][0], ind[h][1] 
            for (x, y), value in zip(circle_centers, data_values):
                if value == np.inf:
                    color = 'white' #'#fee28f' #'lemonchiffon' #'#feeb9d' 
                else:
                    color =   cmap(norm(value)) #'#3d95b8' #'#52abae'#'#79c9a5'#'seagreen' # Get color based on data value
                circle = Circle((x, y), radius, color=color,  lw=0.5)
                ax[u,v].add_patch(circle)
                
            
            # Set limits and aspect ratio
            ax[u,v].set_xlim(-radius, cols * h_spacing)
            ax[u,v].set_ylim(-radius, rows * v_spacing)
            ax[u,v].set_aspect('equal')


            clr, outline = 'black', 'gray'#'palegreen' #'darkseagreen' #paleturquoise
            if h == 0:
                clr = 'black'#'darkred'
                outline = 'gray'#'bisque'

            # Setting font dictionary  
            font = {'family': "Times New Roman",
                    'color':  clr, 
                    'size': 15,
                    }               
            # Adding the font styles to the label
            ax[u,v].set_ylabel(f'{labels[h]}', fontdict=font)
                  
            for side in ['top','right','bottom','left']:
            #ax[u,v].spines[side].set_visible(False)
                ax[u,v].spines[side].set_color(outline) 
            ax[u,v].spines['left'].set_position(('outward', 2))
            ax[u,v].spines['bottom'].set_position(('outward', 2.5)) 
            ax[u,v].tick_params(axis='both',which='both',labelbottom=False,\
                            labelleft=False, bottom=False,left=False)
            plt.tight_layout() #controls the margin of the overall figure

##        # Step 5: Add a colorbar
##        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
##        sm.set_array([])
##        cbar = plt.colorbar(sm, location='bottom')
##        cbar.set_label(label="time $t$*", fontsize=14)
##        cbar.ax.tick_params(labelsize=14)

        #plt.title(f'{distn[h]}, sigma={sig}, lambda={lambd}')
        print(f'\nsigma={sig}, lambda={lambd}')

        fig.set_dpi(500.0)  # This controls display resolution

        fig.subplots_adjust(wspace=0.1, hspace=0.025) #adjusts the distances between subplots in each figure
        fig.savefig(f'_(0)_evolution_plot_sigma={sig}_lambda={lambd}.png', dpi=500)  # , bbox_inches='tight' # Ensures saved file has 500 dpi

        plt.show()

