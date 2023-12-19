from minimizing_parabola import best_k_parabols
import numpy as np

# Input:
# P - n by n matrix that [i][j] cell is the parabola that minimizing the distances of points i to j from her
# D - n by n matrix that [i][j] cell is the distance between node i and node j,
# the distance defined as the squared residuals of the points from the parabola P[i][j]
#
# Output:
# k - the optimal number k of parabolas
# parabolas, residuals, shortestPath - the parabolas ,residual and shortestPath for that k, generated by best_k_parabols() function
#
# Complexity;
# time: O(n)<  //    usualy is much less
# memory: O(n)< //   "                 "
#
def find_optimal_k(P, D):
    n = len(D)
    
    # array f the residuals for each k
    distortions = []
    
    # computing residuals for k = 1
    k = 1
    #  parameters that storing for k = 1
    first_parabolas, first_residuals, first_shortestPath = best_k_parabols(P, D, k)
    #  parameters that storing for the last k that was running
    last_parabolas, last_residuals, last_shortestPath = first_parabolas, first_residuals, first_shortestPath
    loss = np.sum(first_residuals)
    distortions.append(loss)
    
    elbow_point = None
    
    # max posible clusters in this problemis n/2, becaue to use the polyfit(points) function, you need at least 2 points
    max_clusters = int(n/2)
    # elbow method
    # computing the optimal k for the best k parabols with best_k_parabols function:
    # We identify the "elbow" point by finding the index where the difference in distortions falls below a threshold
    # in this example, 10% of the mean difference.
    for k in range(2, max_clusters+1):
        parabolas, residuals, shortestPath = last_parabolas, last_residuals, last_shortestPath
        last_parabolas, last_residuals, last_shortestPath = best_k_parabols(P, D, k)
        loss = np.sum(last_residuals)
        distortions.append(loss)
        # Check for the elbow point
        if abs(distortions[k - 2] - distortions[k - 1]) <= np.mean(abs(np.diff(distortions))) * 0.05:
            elbow_point = k - 1
            break
        
    # If the optimal k is 1, set elbow_point to 1
    if distortions[0] <= np.mean(distortions) * 0.1: 
        elbow_point = 1
        parabolas, residuals, shortestPath = first_parabolas, first_residuals, first_shortestPath
        
    # if elbow point is not found
    if(elbow_point == None):
        elbow_point = max_clusters
        parabolas, residuals, shortestPath = last_parabolas, last_residuals, last_shortestPath
                       
    k = elbow_point
    
    return parabolas, residuals, shortestPath, k