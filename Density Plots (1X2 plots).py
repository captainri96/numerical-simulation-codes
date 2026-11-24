import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

print("\nHere is a list of the different cropping arrangements:\n")
patterns = {0: 'Monocrop', 1: 'Row', 2: 'Diagonal', 3: 'Row Strips', 4: 'Column Strips', 5: 'Patches'}
print(patterns)

lambdA = int(input('\nEnter value of lambda: '))

# Load data
df1 = pd.read_csv(r'Density_plots_Mono.csv')
monos = df1.to_numpy()
monos = monos[:, 1:]

df2 = pd.read_csv(fr'Density_plots_Markovian_L{lambdA}.csv')
dens = df2.to_numpy()
dens = dens[:, 1:]

# Files and cropping arrangements
csv_files = ['mono', 0, 2, 4, 6, 8]


# List of colors to use in each plot
########colors = ["magma", "viridis", "pink", "coolwarm", "Blues", "cividis"] #

if lambdA == 1:
    colors = ["magma", "viridis", "viridis", "viridis", "viridis", "viridis"]
    
    
elif lambdA == 2:
    colors = ["magma", "RdYlGn", "RdYlGn", "RdYlGn", "RdYlGn", "RdYlGn"]

else:
##    colors = ["magma", "Set2", "Set2", "Set2", "Set2", "Set2"]
    colors = ["magma", "coolwarm", "coolwarm", "coolwarm", "coolwarm", "coolwarm"]



for q in [0, 2, 4]:
    loop_plots = [q, q+1]   #for each plot in a 1x2 figure
    colours = [colors[q], colors[q+1]]             
    

    sns.set_style("white")                          # Set Seaborn style
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.5)) # Create 2x3 grid of subplots
    
    # Iterate over the axes, files, and colors
    for ax, plot, color in zip(axes.flatten(), loop_plots, colours):
        print('csv_file:', csv_files[plot])
        
        # Generate data for each plot based on csv_file index
        if csv_files[plot] == 'mono':  # Data from 'mono' (Monocrop)
            data1 = monos[:1000, 0]
            data2 = monos[:1000, 1]
            
            # Create a DataFrame
            df = pd.DataFrame({'Markovian time $t*$': np.concatenate([data1, data2]),
                               'mobility': ['\u03C3 $=$ 2.5'] * 1000 + ['\u03C3 $=$ 4.0'] * 1000})
            title = 'Monocrop'  # Custom title for monocrop

        else:  # Data from 'dens' (Markovian)
            data1 = dens[:500, csv_files[plot]]
            data2 = dens[:500, csv_files[plot] + 1]
            
            # Create a DataFrame
            df = pd.DataFrame({'Markovian time $t*$': np.concatenate([data1, data2]),
                               'mobility': ['\u03C3 $=$ 2.5'] * 500 + ['\u03C3 $=$ 4.0'] * 500})
            
            #k = (csv_file//2)+1
            title = patterns[plot]  # Use label from cropping arrangements dictionary

        # Create the density plot
        sns.kdeplot(data=df, x="Markovian time $t*$", hue="mobility", fill=True, alpha=0.7, palette=color, ax=ax, common_norm=False)
        
        # Add a title for each subplot
        ax.set_title(f"{title}", fontdict={'family': 'Times New Roman', 'weight': 'bold', 'size': 14})

        # Manually add the legend to each subplot
        if lambdA == 5 and csv_files[plot] != 'mono':
            ax.legend(title=None, loc='upper left', labels=['\u03C3 $=$ 2.5', '\u03C3 $=$ 4.0'])
        
        
        # Remove spines for a cleaner look
        #sns.despine(ax=ax)

        legend = ax.get_legend()
        if legend:
            legend.set_title(None)

        ax.set_xlim(1, 105) # Set x-axis range
        ax.set_ylim(0, 0.21) # Set y-axis range

    # Adjust layout for better spacing
    plt.tight_layout()

    # Adjusts the distances between subplots in each figure
    fig.subplots_adjust(wspace=0.32, hspace=0.3)

    # Set display resolution
    fig.set_dpi(500.0)

    fig.savefig(f'(0)_density_plot_{q//2+1}_lambda={lambdA}.png', dpi=500)

    # Show the plot
    #plt.show()
