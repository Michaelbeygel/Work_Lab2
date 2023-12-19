import numpy as np



# Input:
# D - n by n matrix that [i][j] cell is the distance between node i and node j
# k - integer > 1 represent length of the path 
#
# Output:
# minDist - shortest distance of length k from node 1 to node n
# shortestPath - vector of k-1 length of indexes for the shortest path
#
# Complexity;
# time: O(kn^2)
# memory: O(nk)
#
# Explain:
# F[m][i] = shoertest way to node i with m steps
# = min{j=1 : n} (F(m-1, j) + D[i][j])
#
def shortest_k_path(D, k):   


    n = len(D[0])
    F = np.zeros((k,n))
    P = np.zeros((k,n), dtype=int)

   # Initialize the first row of F with values from D
    for i in range(n):
        F[0][i] = D[0][i]
        P[0][i] = i

    # Calculate F(m, i) for m from 1 to k-1
    for m in range(1, k):
        for i in range(n):
            min_val = float('inf')
            lastIndex = -1
            for j in range(i-1):
                temp = F[m - 1][j] + D[i][j+1]
                if temp < min_val:
                    min_val = temp
                    lastIndex = j
            F[m][i] = min_val
            P[m][i] = lastIndex
    

    shortestPath = computePath(P, P[k-1, n-1])

    return F[k-1, n-1], shortestPath


# Input:
# P - n by n matrix that [i][j] cell is the distance between node i and node j
# goal - the last node in the optimal path to n
#
# Output:
# shortestPath - vector of length k-1 with the k-1 indexed of the shortest path from node 1 to node n
#
# Complexity;
# time: O(k)
# memory: O(k)
#
def computePath(P, node):
    k = len(P)
    if(k == 1):
        return []
    
    shortestPath = np.zeros(k - 1, dtype=int)
    for i in range(k - 1):
        shortestPath[k - i - 2] = node
        if k - i - 2 != 0:
            node = P[k - i - 2][node]
    return shortestPath









