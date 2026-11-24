import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import sys
import csv


m, n = 19, 98 #7,18  #9, 24  #9, 198
#n is even no. of column of equilateral triangles, m is odd rows of equi.triangles
lattice_type = 'hexagonal'

G = nx.triangular_lattice_graph(m, n, periodic=False,\
        with_positions=True, create_using=None)
pos = nx.get_node_attributes(G, 'pos')
mapping = dict(zip(G, range(1,G.order()+1)))
H = nx.to_numpy_array(G, dtype='f')

# Python program for Dijkstra's single source shortest path algorithm.
# The program is for the adjacency matrix representation of the graph.

for each_crop_src in range(G.order()): #G.order() computes total nodes in a lattice
    class Graph():

            def __init__(self, vertices):
                    self.V = vertices
                    self.graph = [[0 for column in range(vertices)]
                                            for row in range(vertices)]

    ##	def printSolution(self, dist):
    ##		print("Vertex \tDistance from Source")
    ##		for node in range(self.V):
    ##			print(node, "\t", dist[node])

            # A utility function to find the vertex with minimum distance value,
            # from the set of vertices not yet included in shortest path tree
            def minDistance(self, dist, sptSet):

                    # Initialize minimum distance for next node
                    min = sys.maxsize

                    # Search not nearest vertex not in the shortest path tree
                    for u in range(self.V):
                            if dist[u] < min and sptSet[u] == False:
                                    min = dist[u]
                                    min_index = u

                    return min_index

            # Function that implements Dijkstra's single source shortest path algorithm for a graph
            # represented using adjacency matrix representation
            def dijkstra(self, src):

                    dist = [sys.maxsize] * self.V
                    dist[src] = 0
                    sptSet = [False] * self.V

                    for cout in range(self.V):

                            # Pick the minimum distance vertex from the set of vertices not yet
                            # processed. x is always equal to src in first iteration
                            x = self.minDistance(dist, sptSet)

                            # Put the minimum distance vertex in the shortest path tree
                            sptSet[x] = True

                            # Update dist value of the adjacent vertices of the picked vertex only if
                            # the current distance is greater than new distance and the vertex in not
                            # in the shortest path tree.
                            for y in range(self.V):
                                    if self.graph[x][y] > 0 and sptSet[y] == False and \
                                                    dist[y] > dist[x] + self.graph[x][y]:
                                            dist[y] = dist[x] + self.graph[x][y]
                                            H[each_crop_src, y] = dist[y]
                                            H[y, each_crop_src] = dist[y]
    ##		self.printSolution(dist)
    # Driver's code
    if __name__ == "__main__":
            g = Graph(len(H))
            g.graph = H
            g.dijkstra(each_crop_src)

##    #ENDOFCLASS


#print('\n\nThe "Mellin d-transformed" adjacency matrix A_tilde')
#print('of a',lattice_type,'lattice is:\n')
#print(H)

#dimensions = H.shape
#rows, columns = dimensions

#print("Rows:", rows)
#print("Columns:", columns)

font = 'teal'#'mediumseagreen'#'seagreen' # 'lemonchiffon' # 'yellowgreen'
options = {"edgecolors": "darkslategray", "node_size": 140}
#options = {"edgecolors": "darkslategray", "node_size": 400}
nx.draw(G,pos=pos, labels=mapping, node_color=font, \
        font_size=0, font_color = font, width=1, **options)
plt.show()

N = G.order() #total no. of crops
print(f'\nTotal number of crops (main and secondary): {N}')
#return(H,m,n,N)  #H is the matrix operator Aij

A_ij = pd.DataFrame(H)
A_ij.to_csv("A_ij.csv")
