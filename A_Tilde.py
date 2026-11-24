import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import math
import sys
import csv
import pandas as pd
import os

##df = pd.read_csv(r'C:\Users\User\Desktop\(3rd run) seir_ markovian\A_ij.csv')
df = pd.read_csv(r'A_ij.csv')
A_ij = df.to_numpy()
Aij = A_ij[:,1:]

def A_hex(sigma,lamBda,arrangement):
    m, n, N  = 19, 98, 1000
    A_tilde = np.zeros((N,N), dtype='f')
    total_rows = m+1
    nodes_per_row = int((n/2)+1)
    main_cultivar = []
    

    def params(expon):
        for i in range(0,N):
            for j in range(i,N):
                if i!=j:
                    A_tilde[i,j] = Aij[i,j]**(expon)

    
    if arrangement == 0: #monocrop
        params(-sigma)   #invokes call for 'params' to incorporate parameter sigma
        main_cultivar = [plant for plant in range(N)]

 
    if arrangement == 1: #row/column
        params(-sigma*lamBda)      
        for ith_row in range(0,total_rows):     
            if ith_row%2 == 0: #odd-rows
                ith_node = ith_row * nodes_per_row
                nodes = [i+ith_node for i in range(nodes_per_row)]
                main_cultivar.extend(nodes)
                for i in range(ith_node, (ith_node + nodes_per_row)):
                    for j in range(i+1,(ith_node + nodes_per_row)):
                        A_tilde[i,j] = Aij[i,j]**(-sigma)
                        #print(f'A[i,j] = A[{i+1}, {j+1}]')
                
                
    #***obtaining the Boundary points***
    boundary = []
    boundary.extend([bottom for bottom in range(nodes_per_row)])                #bottom bdry points
    boundary.extend([top for top in range(N-nodes_per_row,N)])                  #top bdry points
    boundary.extend([(left*nodes_per_row) for left in range(1,total_rows-1)])   #left bdry points
    boundary.extend([((right*nodes_per_row)+nodes_per_row-1) for right in range(1,total_rows-1)])                       #right bdry points
    #******
    #print('boundary:\n', boundary)

    if arrangement == 2: #diagonal
        params(-sigma*lamBda)
        diagonals, increm = [], 0
        main_cultivar = [0]

        total_diagonals = int(nodes_per_row/2) + int(total_rows//4)
        #print(total_diagonals)
        main_culti = [[] for i in range(total_diagonals+1)]
        maize, diag = 0, 0

        for x in range(total_rows):
            #print(f'\n\n\n{x+1}th row: ', diag)
            for y in range(int(nodes_per_row/2)):
                main_culti[diag+y].extend([maize])
                #print('diag+y: ', diag+y)
                maize += 2
            #print('main_cultivar:\n',main_culti)
            maize -= 2
            
            if x%4==0:
                maize += 3
            elif x%4==1 or x%4==3:
                maize += 2
            else: #x%4==2
                maize += 1

            if x==0:
                diag+=1
            elif (x>1 and x<total_rows-1):
                #print('main_culti[diag][-1]: ', main_culti[diag][-1])
                #print('main_culti[diag][-2]: ', main_culti[diag][-2])
                if (main_culti[diag][-1] and main_culti[diag][-2]) in boundary:
                    diag+=1
            else:
                continue
        #print('\n\nmain_cultivar:\n',main_culti)

        main_cultivar = [0]
        for each in range(1,len(main_culti)):
            lisT = main_culti[each]
            main_cultivar.extend(lisT)
            for j in range(len(lisT)-1):
                for k in range(j+1,len(lisT)):
                    A_tilde[lisT[j],lisT[k]] = Aij[lisT[j],lisT[k]]**(-sigma)
                    #print(f'A[i,j ] = A[{lisT[j]+1}, {lisT[k]+1}]')
            #print('\n')
        #print('main_cultivar:\n', main_cultivar)



    if arrangement == 3: #row strips
        params(-sigma*lamBda)
        for ith_row_strip in range(0,int(total_rows/2)):
            if ith_row_strip%2 == 0: #odd row strips
                ith_node = ith_row_strip * 2* nodes_per_row
                nodes = [i+ith_node for i in range(2*nodes_per_row)]
                #print(f'\n{ith_row_strip}:', nodes)
                main_cultivar.extend(nodes)
                
                for i in range(ith_node, (ith_node+(2*nodes_per_row))):
                    for j in range(i+1,(ith_node+(2*nodes_per_row))):
                        A_tilde[i,j] = Aij[i,j]**(-sigma)
                        #print(f'A[i,j] = A[{i+1}, {j+1}]={Aij[i,j]**(-sigma)}')
        #print('\nmain_cultivar (row strips):\n',main_cultivar)


    if arrangement == 4: #column strips
        params(-sigma*lamBda)
        k, p = 0,0
        
        for ith_col_strip in range(0,nodes_per_row):
            if ith_col_strip%2 == 0: #odd column strip
                base_node = ith_col_strip
                column = [base_node + (k*nodes_per_row) for k in range(total_rows)]
                for i in range(len(column)-1):
                    A_tilde[column[i],column[i+1]] = Aij[column[i],column[i+1]]**(-sigma)
                    #print(f'A[i,j] = A[{column[i]+1}, {column[i+1]+1}]')
                #print('')

                if ith_col_strip == 0:
                    for m in range(0,int(len(column)/2)-1):
                        A_tilde[column[k],column[k+2]] = Aij[column[k],column[k+2]]**(-sigma)
                        #print(f'A[i,j] = A[{column[k]+1}, {column[k+2]+1}]\n')
                        k+=2

                if ith_col_strip == nodes_per_row-1:
                    for n in range(0,int(len(column)/2)-1):
                        A_tilde[column[p+1],column[p+3]] = Aij[column[p+1],column[p+3]]**(-sigma)
                        #print(f'\nA[i,j] = A[{column[p+1]+1}, {column[p+3]+1}]\n')
                        p+=2
                main_cultivar.extend(column)


    if arrangement == 5: #patches
        params(-sigma*lamBda)
        ro = nodes_per_row
        k, t, base, left_base = 0, 0, 4, ro*4
        
        def upd_A(k):
            A_tilde[k,k+1] = Aij[k,k+1]**(-sigma) 
            A_tilde[k,k+ro] = Aij[k,k+ro]**(-sigma) 
            A_tilde[k,k+ro+1] = Aij[k,k+ro+1]**(-sigma) 
            A_tilde[k+1,k+ro] = Aij[k+1,k+ro]**(-sigma) 
            A_tilde[k+1,k+ro+1] = Aij[k+1,k+ro+1]**(-sigma) 
            A_tilde[k+ro,k+ro+1] = Aij[k+ro,k+ro+1]**(-sigma) 
            #print(f'A[i,j] = A[{k+1}, {k+2}]')
            #print(f'A[i,j] = A[{k+1}, {k+ro+1}]')
            #print(f'A[i,j] = A[{k+1}, {k+ro+2}]')
            #print(f'A[i,j] = A[{k+2}, {k+ro+1}]')
            #print(f'A[i,j] = A[{k+2}, {k+ro+2}]')
            #print(f'A[i,j] = A[{k+ro+1}, {k+ro+2}]\n')

            main_cultivar.extend([k,k+1,k+ro,k+ro+1]) 
            if k==0:
                go_next_patch = True
            else:      
                if ((k and k+1) and (k and k+1) and (k+1 and k+ro+1) and (k+ro and k+ro+1)) in boundary:
                   go_next_patch = False
                else:
                    go_next_patch = True
            return(go_next_patch)

        def connecting_path(t):
            A_tilde[t+ro+1,t+(2*(ro+1))] = Aij[t+ro+1,t+(2*(ro+1))]**(-sigma)
            A_tilde[t+ro+1,(t+(3*ro)+2)] = Aij[t+ro+1,(t+(3*ro)+2)]**(-sigma)
            A_tilde[t+1,(t+(3*ro)+2)] = Aij[t+1,(t+(3*ro)+2)]**(-sigma)
            #print(f'\nA[i,j]_ = A[{t+ro+2},{t+(2*(ro+1))+1}]')
            #print(f'A[i,j]_ = A[{t+ro+2},{t+(3*ro)+3}]')
            #print(f'A[i,j]_ = A[{t+2},{t+(3*ro)+3}]')


        #main diagonal strip #print("Main diagonal strip\n")
        #print('\nMain diagonal:\n')
        for x in range(0, int(total_rows/2)):
            next_patch = upd_A(k)  
            if (next_patch == True):
                connecting_path(k)
            k = k+(2*(ro+1))


        #right-side diagonal strips #print("\nRight-side diagonal strip\n")
        #print('\nRight side:\n')
        if (ro-4)%4!=0:
            end = ((ro-4)//4) + 1
        else:
            end = (ro-4)//4
            
        for y in range(0, end):
            t =  base
            for z in range(0,int(total_rows/2)):
                if (t in boundary) and (t+ro in boundary): #checking first patch's left side
                    A_tilde[t,t+ro] = Aij[t,t+ro]**(-sigma)
                    #print(f'\nA[i,j]& = A[{t+1},{t+ro+1}]\n')
                    main_cultivar.extend([t,t+ro])
                    break
                elif (t+1 in boundary) and (t+ro+1 in boundary): #checking first patch's right side
                    next_patch = upd_A(t)
                    break         
                elif (t+ro in boundary) and (t+ro+1 in boundary): #checking patch's upper side
                    next_patch = upd_A(t)
                    break
                else:
                    next_patch = upd_A(t)
                    if (next_patch == True):
                        connecting_path(t)
                t = t+(2*(ro+1))
            base += 4 #updating base node for each diag  

        #left-side diagonal strips #print("\nLeft-side diagonal strip\n")
        #print('\nLeft side:\n')
        if (total_rows-4)%4!=0:
            top_end = ((total_rows-4)//4) + 1
        else:
            top_end = (total_rows-4)//4

        for p in range(0,top_end):
            t =  left_base
            for q in range(0,int(total_rows/2)):
                if (t+ro in boundary) and (t+ro+1 in boundary): #checking first patch's upper side
                    next_patch = upd_A(t)
                    break         
                else: 
                    next_patch = upd_A(t)
                    if (next_patch == True):
                        connecting_path(t)
                    t = t+(2*(ro+1))
            left_base += ro*4 #updating base node for each diag
                

    #Transpose of matrix A_tilde               
    for i in range(0,N):
        for j in range(i,N):
            A_tilde[j,i] = A_tilde[i,j]

    return (A_tilde, main_cultivar)
                


"""MAIN"""

print("\nHere is a list of the different cropping arrangements:\n")
distn = {0:'Monocrop', 1:'Rows_Columns', 2:'Diagonal',\
         3:'Row strips', 4:'Column strips', 5:'Patches'}
print(distn)

#sigma, lambdA = 4, 1  
sig = [2.5, 4] #insect mobility: # 1.0, 2.5, 4.0 -> poor mobility
lambd = [1, 2, 5] #trap strength: 1.0, 2.0, 5 +inf  -> perfect trap strength
##sig, lambd = [2.5, 4], [10]

secondary = np.full((1000,6),0, dtype = 'f')
column_name =['Mono', 'Ro_Cols','Diag', 'RowStps', 'ColStps','Pat']
m, n, N = 19, 98, 1000

print('\n')
for s in sig:
    for l in lambd:
        for pattern in range(6):
            title = distn[pattern]
            
            aij_Tilde, main_crop = A_hex(s, l, pattern)
            print(f'sigma={s}, lambda={l}, pattern = {distn[pattern]}')

            A_Tilde = pd.DataFrame(aij_Tilde)
            A_Tilde.to_csv(f"A_tilde_ sigma={s},lambda={l},{distn[pattern]}.csv")

            # Finding TRAP Crops:
##            if (s == 2.5) and (l == 1):
##                #determining all sacrificial/secondary crops
##                print(f'\n{pattern+1}. Intercropping pattern: {title}')
##                all_crops = [p for p in range(N)]
##                print(f'\nmain crops: ', len(main_crop))
##                trap_crops = list(filter(lambda x: x not in main_crop, all_crops))
##                print(f'\ntotal trap crops: ',len(trap_crops))
##
##                #The purpose of the ff. lines is to convert the values of nodes 
##                #to "inf" when they are identified as a trap crop.
##                for each in trap_crops:
##                    for j in range(1000):
##                        if each == j:
##                            secondary[j,pattern] = np.inf
##
##                total_row_nodes = int((n/2+1))
##                traps = pd.DataFrame(secondary, columns=column_name)
##                traps.to_csv(f'Trap_crops_{m+1}_by_{total_row_nodes}_field.csv')
        print('\n')

    


