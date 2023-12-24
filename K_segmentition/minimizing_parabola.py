import numpy as np
from path_algo.k_shortest_path import shortest_k_path


# Input:
# D - n by n matrix that [i][j] cell is the distance between node i and node j,
# the distance defined as the squared residuals of the points from the parabola that minimizing the distances of points i to j from the parabola
# P - n by n matrix that [i][j] cell is the parabola that minimizing the distances of points i to j from her
# k - number of parabolas wanted
#
# Output:
# parabolas - array of k parabolas that minimizing the sum of distances of the points
# residuals - array ith -  sum of distances of the points with index shortestPath[i]+1 to shortestPath[i+1] to parbola[i]
# shortestPath - the indexes of the parabolas start and end
#
# Complexity;
# time: O(kn^2)
# memory: O(kn)
# 
def best_k_parabols(D, P, k):

    n = len(D)

    minDist, shortestPath = shortest_k_path(D, k) 

    parabolas = []  # List to store the fitted parabolas
    residuals = []  # List to store the sum of squared residuals for each segment
    if k > 1:
        start_idx = 0
        for i in range(k-1):
            end_idx = shortestPath[i]
    
            parabola = P[start_idx][end_idx]
            residual = D[start_idx][end_idx]
    
            # Fit a parabola to the segment
            parabolas.append(parabola)
            residuals.append(residual)
    
            start_idx = end_idx + 1
    
    
        start_idx = shortestPath[k-2] + 1
        end_idx = n-1
        parabola = P[start_idx][end_idx]
        residual = D[start_idx][end_idx]
    
        parabolas.append(parabola)
        residuals.append(residual)
    else:
        parabola = P[0][n-1]
        residual = D[0][n-1]
    
        # Fit a parabola to the segment
        parabolas.append(parabola)
        residuals.append(residual)


    return parabolas, residuals, shortestPath