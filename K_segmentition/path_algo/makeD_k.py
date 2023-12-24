import numpy as np

def makeD_k(D_1, k):
    n = len(D_1)
    D_k = D_1
    for i in range(1,k):
        D_k = make_next_D(D_k, i, D_1, n)
    return D_k 
    
def make_next_D(current_D, current_k, D_1, n):
    next_D = np.zeros((n,n))
    for i in range(0,n-1):
        for j in range(i+1, n):           
            min_val = float('inf')
            for m in range(i+1, j-1):
                # indexes dif between nodes have to be more than 2, polyfit function dont work with 1 point
                idx_dif = m-i+1
                if idx_dif < 2*current_k or j-m < 2:
                    continue
                temp = D_1[i][m] + current_D[m+1][j]
                if temp < min_val:
                    min_val = temp
            next_D[i][j] = min_val
    
    return next_D
                
                
                
