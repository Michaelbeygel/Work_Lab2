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
def k_shortest_path_with_translation_point(asymmetric_D, D_k, k):   
    n = len(asymmetric_D)

    # Calculate F(m, i) for m from 1 to k-1\
    min_val = float('inf')
    translation = -1
    for i in range(0, n-1):
        for j in range(i+1, n):
            # indexes dif between nodes have to be more than 2, polyfit function dont work with 1 point
            idx_dif = j-i+1
            if idx_dif < 2*k or n-idx_dif<2:
                continue

            temp = D_k[i][j] + asymmetric_D[(j+1)%n][i-1]
            if temp < min_val:
                min_val = temp
                translation = j

    return translation


