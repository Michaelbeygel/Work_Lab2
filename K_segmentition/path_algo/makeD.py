import numpy as np
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
# time: O(n^2) * time complexity of polyfit(x, y)
# memory: O(n^2) * memory of polyfit(x, y)
#

def makeD(x_coordinates, y_coordinates):

    n = len(x_coordinates)
    D = np.zeros((n,n))
    P = np.zeros((n, n), dtype=np.poly1d)

    for i in range(0,n-1):
       # initilizizng AtA and AtY matri
        Sx = x_coordinates[i]
        Sxx = x_coordinates[i] ** 2
        Sxxx = x_coordinates[i] ** 3
        Sxxxx = x_coordinates[i] ** 4
        Sy = y_coordinates[i]
        Syy = y_coordinates[i] ** 2
        Sxy = x_coordinates[i] * y_coordinates[i]
        Sxxy = y_coordinates[i] * x_coordinates[i] ** 2
        ## matrix n by d-1(d is the demention here is 2) that first column is 1, second is x coordinates of the points, third column is squered x coordinates
        #A = i row is [1, x_coordinates[i], x_coordinates[i] ** 2]
        ## vector of the y coordinates
        #b = i row is [y_coordinates[i]]
        
        for j in range(i+1, n):            
            # updating AtA and AtY matrix when new point come in 
            Sx += x_coordinates[j]
            Sxx += x_coordinates[j] ** 2
            Sxxx += x_coordinates[j] ** 3
            Sxxxx += x_coordinates[j] ** 4
            Sy += y_coordinates[j]
            Syy += y_coordinates[j] ** 2
            Sxy += x_coordinates[j] * y_coordinates[j]
            Sxxy += y_coordinates[j] * x_coordinates[j] ** 2
            
            AtA = [[j-i+1,  Sx,     Sxx],
                   [Sx,     Sxx,    Sxxx],
                   [Sxx,    Sxxx,   Sxxxx]]
            AtY = [[Sy],
                   [Sxy],
                   [Sxxy]]
            
            
            # make USVT for AtA using svd method
            U, S, VT =  np.linalg.svd(AtA, full_matrices=0)

            # compute inverse of USVT
            inv_of_USVT = ((np.transpose(VT)).dot(np.linalg.pinv(np.diag(S)))).dot(np.transpose(U))
            
            # find x in: AtAx = AtY
            # x = AtA_+ * AtY      
            coefficients = inv_of_USVT.dot(AtY)       

            # transpose the coefficients array         
            coefficients_T = coefficients[:,0] 
            B0 = coefficients_T[0]
            B1 = coefficients_T[1]
            B2 = coefficients_T[2]
            residuals = Syy - 2 * coefficients_T.dot(AtY) + (coefficients_T.dot(AtA)).dot(coefficients)
            parabola = np.poly1d([B2, B1, B0])
                         
            D[i][j] = residuals
            D[j][i] = residuals
            P[i][j] = parabola
            P[j][i] = parabola
        
            

    return D, P; 
