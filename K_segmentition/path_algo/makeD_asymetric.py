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
# time: O(n^2)
# memory: O(n^2)
#
def makeD_asymetric(x_coordinates, y_coordinates):
    
    n = len(x_coordinates)
    D = np.zeros((n,n))
    P = np.zeros((n, n), dtype=np.poly1d)
    
    # initilizizng vars for sum all the points
    all_Sx = 0
    all_Sxx = 0
    all_Sxxx = 0
    all_Sxxxx = 0
    all_Sy = 0
    all_Syy = 0
    all_Sxy = 0
    all_Sxxy = 0
    # sum all the points
    for k in range(n):
        all_Sx += x_coordinates[k]
        all_Sxx += x_coordinates[k] ** 2
        all_Sxxx += x_coordinates[k] ** 3
        all_Sxxxx += x_coordinates[k] ** 4
        all_Sy += y_coordinates[k]
        all_Syy += y_coordinates[k] ** 2
        all_Sxy += x_coordinates[k] * y_coordinates[k]
        all_Sxxy += y_coordinates[k] * x_coordinates[k] ** 2
        
        
    
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
            
            
            #
            #
            # do all over again for case i>j
            #
            #
            AtA_rest = [[n-j+i-1,          all_Sx - Sx,          all_Sxx - Sxx],
                        [all_Sx - Sx,      all_Sxx - Sxx,        all_Sxxx - Sxxx],
                        [all_Sxx - Sxx,    all_Sxxx - Sxxx,      all_Sxxxx -  Sxxxx]]
            AtY_rest = [[all_Sy -Sy],
                       [all_Sxy - Sxy],
                       [all_Sxxy - Sxxy]]
            
            
            # make USVT for AtA using svd method
            U, S, VT =  np.linalg.svd(AtA_rest, full_matrices=0)

            # compute inverse of USVT
            inv_of_USVT = ((np.transpose(VT)).dot(np.linalg.pinv(np.diag(S)))).dot(np.transpose(U))
            
            # find x in: AtAx = AtY
            # x = AtA_+ * AtY      
            coefficients = inv_of_USVT.dot(AtY_rest)       

            # transpose the coefficients array         
            coefficients_T = coefficients[:,0] 
            B0 = coefficients_T[0]
            B1 = coefficients_T[1]
            B2 = coefficients_T[2]
            residuals_rest = all_Syy - Syy - 2 * coefficients_T.dot(AtY_rest) + (coefficients_T.dot(AtA_rest)).dot(coefficients)
            parabola_rest = np.poly1d([B2, B1, B0])
            
                
            D[i][j] = residuals
            P[i][j] = parabola
            D[j][i] = residuals_rest        
            P[j][i] = parabola_rest

    return D; 