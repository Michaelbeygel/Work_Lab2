import numpy as np


def One_Segment_Coreset(points_num ,Sx, Sxx, Sxxx, Sxxxx, Sy, Syy, Sxy, Sxxy):
    AtA = [[points_num,  Sx,     Sxx],
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
    cost = Syy - 2 * coefficients_T.dot(AtY) + (coefficients_T.dot(AtA)).dot(coefficients)
    
    return cost[0]
    
    
    
    