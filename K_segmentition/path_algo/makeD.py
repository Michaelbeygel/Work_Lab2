import numpy as np
import copy
from one_segment_class import One_Segment
# Input:
# points - signal of points
#
# Output:
# D - n by n matrix that [i][j] cell is the distance between node i and node j,
# the distance defined as the squared residuals of the points from the parabola that minimizing the distances of points i to j from the parabola
# P - n by n matrix that [i][j] cell is the parabola that minimizing the distances of points i to j from her

# Complexity;
# time: O(n^2)
# memory: O(n^2)
#

def makeD(points):

    n = len(points)
    D = np.zeros((n,n))
    P = np.zeros((n, n), dtype=np.poly1d)

    for i in range(0,n-1):
       # initilizizng AtA and AtY matri
        one_segment = One_Segment()
        one_segment.add_point(points[i])

        ## matrix n by d-1(d is the demention here is 2) that first column is 1, second is x coordinates of the points, third column is squered x coordinates
        #A = i row is [1, x_coordinates[i], x_coordinates[i] ** 2]
        ## vector of the y coordinates
        #b = i row is [y_coordinates[i]]
        
        for j in range(i+1, n):            
            # updating AtA and AtY matrix when new point come in 
            one_segment.add_point(points[j])
            residuals, parabola = one_segment.cost()
                        
            D[i][j] = residuals
            D[j][i] = residuals
            P[i][j] = parabola
            P[j][i] = parabola
        
            

    return D, P; 



# Input:
# n points that i point is (x_coordinates[i], y_coordinates[i])
# x_coordinates - x coordinates of points in increasing order
# y_coordinates - y coordinates of points
#
# Output:
# D - n by n matrix that [i][j] cell is the distance between node i and node j,
# the distance defined as the squared residuals of the points from the parabola that minimizing the distances of points i to j from the parabola
# P - n by n matrix that [i][j] cell is the parabola that minimizing the distances of points i to j from her

# Complexity;
# time: O(n^2)
# memory: O(n^2)
#
def makeD_asymetric(points):
    
    n = len(points)
    D = np.zeros((n,n))
    P = np.zeros((n, n), dtype=np.poly1d)
    
    # initilizizng 1-segement all the points
    rest_points_one_segment = One_Segment()

    # make 1-segment for all the points
    for k in range(n):
        rest_points_one_segment.add_point(points[k])
        
        
    
    for i in range(0,n-1):
        # init the 1-segment from ith point
        one_segment = One_Segment()
        one_segment.add_point(points[i])
        # make a copy of rest point segment without point ith
        rest_segment = copy.copy(rest_points_one_segment)
        rest_segment.remove_point(points[i])

        for j in range(i+1, n):
            # each iteretion we add point and compute the new 1-segment cost of 
            one_segment.add_point(points[j])           
            residuals, parabola = one_segment.cost()

            # each iteretion we remove point from the rest points 1-segment and compute the new cost
            rest_segment.remove_point(points[j])
            residuals_rest, parabola_rest = rest_segment.cost()
            
            # put in the 2D array so its asymetric    
            D[i][j] = residuals
            P[i][j] = parabola
            D[j][i] = residuals_rest        
            P[j][i] = parabola_rest

    return D
