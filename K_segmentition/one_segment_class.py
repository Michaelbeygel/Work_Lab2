import numpy as np

# class that store needed data for 1-segment corset
# needed data is various Sums of x and y of points
class One_Segment:
    def __init__(self):
        self.Sx = 0
        self.Sxx = 0
        self.Sxxx = 0
        self.Sxxxx = 0
        self.Sy = 0
        self.Syy = 0
        self.Sxy = 0
        self.Sxxy = 0
        self.length = 0

    #  new_point - new point that added, so we update all the sums
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
        self.length += 1
    # last_point - remove point, so we update all the sums
    def remove_point(self, last_point):
        new_x = last_point[0]
        new_y =  last_point[1]
        self.Sx -= new_x
        self.Sxx -= new_x**2
        self.Sxxx -= new_x**3
        self.Sxxxx -= new_x**4
        self.Sy -= new_y
        self.Syy -= new_y**2
        self.Sxy -= new_x * new_y
        self.Sxxy -= new_y * new_x**2
        self.length -= 1


    # return - the sse(cost) for the sums of the signal so far, and the parabola
    # d - demention of the signal
    # Time: O(d^3)
    # Space: O(d^2)
    def cost(self):
        AtA = [[self.length,  self.Sx,     self.Sxx],
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

        # store the coeff and create parabola
        B0 = coefficients_T[0]
        B1 = coefficients_T[1]
        B2 = coefficients_T[2]
        parabola = np.poly1d([B2, B1, B0])

        return cost[0], parabola


