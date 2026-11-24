import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Define colormap and normalization from 1 to 100
cmap = plt.get_cmap('RdYlGn')
norm = mcolors.Normalize(vmin=1, vmax=100)

# Create a figure and axis for colorbar
fig, ax = plt.subplots(figsize=(12, 1.1))  # Adjust figure size as needed
fig.subplots_adjust(bottom=0.5)  # Adjust the position

# Create ScalarMappable for colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # Dummy array for the colorbar

# Create horizontal colorbar
cbar = plt.colorbar(sm, cax=ax, orientation='horizontal')

# Ensure all tick labels including 100 are displayed
cbar.set_ticks([1, 20, 40, 60, 80, 100])
cbar.ax.set_xticklabels([1, 20, 40, 60, 80, 100])

# Set colorbar label
cbar.set_label(label='Markovian time $t$*', fontsize=16)
cbar.ax.tick_params(labelsize=16)
plt.tight_layout()
fig.savefig(f'colorbar_RdYlGn_normal.png', dpi=500)

# Show plot
plt.show()
