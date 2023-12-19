import numpy as np

class One_Segment:
    def __init__(self, Sx, Sxx, Sxxx, Sxxxx, Sy, Syy, Sxy, Sxxy):
        self.Sx = Sx
        self.Sxx = Sxx
        self.Sxxx = Sxxx
        self.Sxxxx = Sxxxx
        self.Sy = Sy
        self.Syy = Syy
        self.Sxy = Sxy
        self.Sxxy = Sxxy

    def add_point(self, new_point):
        new_x = new_point[0]
        new_y =  new_point[1]
        self.Sx += new_x
        self.Sxx += new_x**2
        self.Sxxx += new_x**3
        self.Sxxxx += new_x**4
        self.Sy += new_y
        self.Syy += new_y**2
        self.Sxy += new_x * new_y
        self.Sxxy += new_y * new_x**2

    def remove_point(self, new_point):
        new_x = new_point[0]
        new_y =  new_point[1]
        self.Sx -= new_x
        self.Sxx -= new_x**2
        self.Sxxx -= new_x**3
        self.Sxxxx -= new_x**4
        self.Sy -= new_y
        self.Syy -= new_y**2
        self.Sxy -= new_x * new_y
        self.Sxxy -= new_y * new_x**2
    


    def cost(self, points_num):
        AtA = [[points_num,  self.Sx,     self.Sxx],
                     [self.Sx,     self.Sxx,    self.Sxxx],
                   [self.Sxx,    self.Sxxx,   self.Sxxxx]]
        AtY = [[self.Sy],
           [self.Sxy],
           [self.Sxxy]]
             
        # make USVT for AtA using svd method
        U, S, VT =  np.linalg.svd(AtA, full_matrices=0)
        # compute inverse of USVT
        inv_of_USVT = ((np.transpose(VT)).dot(np.linalg.pinv(np.diag(S)))).dot(np.transpose(U))

        # find x in: AtAx = AtY
        # x = AtA_+ * AtY      
        coefficients = inv_of_USVT.dot(AtY)       
        # transpose the coefficients array         
        coefficients_T = coefficients[:,0] 
        cost = self.Syy - 2 * coefficients_T.dot(AtY) + (coefficients_T.dot(AtA)).dot(coefficients)

        return cost[0]


