from matplotlib import pyplot as plt
import numpy as np
from one_segment_class import One_Segment
from optimal_bicriteria import optimal_bicriteria_points
from rectangle_problem.point_in_rectangle import distances
import sys

debug = '-d' in sys.argv or '--debug' in sys.argv


# input: The algorithm gets a signal P and Sigma - number σ which is assumed to be an estimation of the cost of the k-segment mean of P
# output: set D - small parts that each part has the closest cost to Sigma
#
# Time: O(n)
# Space: O(n)
def balanced_partition(points, Sigma):
    print(f"number of points: {len(points)}")
    # set values for 1-segment corset
    D = []
    Q = []
    one_segment = One_Segment()
    # each itereion we update values the new 1-segment corset with the new point added
    for i in range(len(points)):
        
        # add new point
        Q.append(points[i])
        one_segment.add_point(points[i])
        
        # compute 1-segment corset with new point
        cost, parabola = one_segment.cost()

        # if last point include it and calc the cost
        if i == len(points)-1:
            D.append((cost, i-len(Q), i))
            continue
        
        # 
        if cost > Sigma:
            # then we take the previous cost - without the new point
            T = Q
            T.pop()       
            one_segment.remove_point(points[i])     

            # compute 1-segment corset without the new point
            cost, parabola = one_segment.cost()

            D.append((cost, i-len(T), i-1))
            
            
            # reset values for 1-segment corset and start compute from ith point
            Q = [points[i]]
            one_segment = One_Segment()
            one_segment.add_point(points[i])
    return D





def test_balanced_partition():
    if __name__ == '__main__':           
        # aproximate parabolas that we make point around them
        rectangle = [(0,0), (100,90)] # rectangle attached to points (0,0) and (20,25)
        p = (50, 45)  # Coordinates of point p within the rectangle
        angle_distance_arr = distances(rectangle, p)
        points1 = []
        for point in angle_distance_arr:
            if point[1] != float('inf'):
                points1.append(point)
            
        k = 5
               
        copy_points = np.array(points1)   
        
        Sigma = optimal_bicriteria_points(points1, k)
        print(f"Sigma is: {Sigma}")
        D = balanced_partition(copy_points, Sigma)
        print(f"number of parts in D: {len(D)}")
        print(D)
        
        if debug:
            x_coordinates = [point[0] for point in copy_points]
            y_coordinates = [point[1] for point in copy_points]
            plt.figure(f'points with Sigma: {Sigma}')
            plt.plot(x_coordinates, y_coordinates, '.', color = 'black')
            xs = np.linspace(30, 80, 100)
            x_dividers = [x_coordinates[D[i][1]] for i in range(1,len(D))]
            plt.vlines(x=x_dividers, ymin=0, ymax=len(xs), colors='purple', ls='--', lw=2, label='vline_multiple - full height')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.legend(f"points with Sigma: {Sigma}")
            plt.title(f'points with Sigma: {Sigma}')
            plt.show()
        
        
        
        
test_balanced_partition()