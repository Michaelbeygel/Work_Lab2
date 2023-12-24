#import random
#from rectangle_problem.point_in_rectangle import distances
import random
from matplotlib import pyplot as plt
import numpy as np
import warnings
import sys
from rectangle_problem.point_in_rectangle import distances
# Filter out RankWarning
warnings.filterwarnings("ignore", category= np.RankWarning)

debug = '-d' in sys.argv or '--debug' in sys.argv

# input: signal - points and integer k
# output: Sigma - assumed to be an estimation of the cost of the k-segment mean of P
# 
# Time: O(n)
# Space: O(n)
#
# explain: divide the signal into NUMBER_OF_SUB_PARTS sub-intervals, where each interval contain the same number of input points.
# compute the 1-segment mean of each part
# then pick the set Q of NUMBER_OF_BEST_PARTS_TAKEN sub-intervals whose approximated cost to their 1-segment mean is minimal
# then We then continue recursively with the remaining points
def optimal_bicriteria_points(points, k):

    NUMBER_OF_SUB_PARTS = 4*k # integer number of part the signal will divided each time
    NUMBER_OF_BEST_PARTS_TAKEN = k+1 # integer number of best parts(minimal cost) that taken each iteretion
    opt_rse = 0
    iteretion = 1

    while len(points)/NUMBER_OF_SUB_PARTS >= 2:        
        x_coordinates = [point[0] for point in points]
        y_coordinates = [point[1] for point in points]

        # plot the points each iteretion(if debug mode)
        if debug:
            print("debug mode on")
            plt.figure(f'Parts: {NUMBER_OF_SUB_PARTS}\nTaken: {NUMBER_OF_BEST_PARTS_TAKEN}')
            plt.plot(x_coordinates, y_coordinates, '.', color = 'black')
        
        # divide to part and store the best(min cost) then remove those parts
        rse, left_points, parabolas_and_x_range = divide_bi_and_get_return_best_parts(points, NUMBER_OF_SUB_PARTS, NUMBER_OF_BEST_PARTS_TAKEN)
        opt_rse += rse
        points = left_points
        

        # plot parabolas if debug mode
        if debug:
            # orgenize the data for the plot
            x = []
            y = []
            parabolas = [tumle[0] for tumle in parabolas_and_x_range]
            for i in range(NUMBER_OF_SUB_PARTS):
                start_x = parabolas_and_x_range[i][1]
                end_x = parabolas_and_x_range[i][2]

                parabola_i_x = []
                parabola_i_y = []
                # create 1000 equally spaced points between the start of the parabola to end to draw the returned parbola more acurate
                parabola_i_x = np.linspace(start_x, end_x, 100)

                # calculate the y value for each element of the x vector
                parabola_i_y = parabolas[i](parabola_i_x)  

                x.append(parabola_i_x)
                y.append(parabola_i_y)
                # generate the Plots

            # plot the parabolas of the parts
            for i in range(NUMBER_OF_SUB_PARTS):
                plt.plot(x[i], y[i]), 
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.legend([f"iteretion {iteretion}"], fontsize="x-large")
            plt.title(f'Parts: {NUMBER_OF_SUB_PARTS}\nTaken: {NUMBER_OF_BEST_PARTS_TAKEN}')
            iteretion += 1
            plt.show()
       
    return opt_rse



# input: signal - points,
# NUMBER_OF_SUB_PARTS - number of parts we divide the signal to
# NUMBER_OF_BEST_PARTS_TAKEN - number of parts taken
#
# output: opt_rse - sum of the cost of the best parts,
# left points - the signal without the best parts,
# parabolas_and_x_range - the parabolas of all the parts and their range(for ploting them later)
#
# Time: O(n)
# Space: O(n)
# n - the length of the signal
#
# explain: divide the signal into NUMBER_OF_SUB_PARTS sub-intervals, where each interval contain the same number of input points.
# compute the 1-segment mean of each part
# then pick the set Q of NUMBER_OF_BEST_PARTS_TAKEN sub-intervals whose approximated cost to their 1-segment mean is minimal
# and remove those part from the signal
def divide_bi_and_get_return_best_parts(points ,NUMBER_OF_SUB_PARTS, NUMBER_OF_BEST_PARTS_TAKEN):   
    sub_parts_tamples = [] # tample of (points[start_idx: end_idx], start_id, end_idx, rse)
    n = len(points)
    parabolas_and_x_range = []
    
    start_idx = 0
    for i in range(1, NUMBER_OF_SUB_PARTS+1):
        # divide to parts
        end_idx = int((n / NUMBER_OF_SUB_PARTS) * i)     
        x = [points[i][0] for i in range(start_idx,end_idx)]
        y = [points[i][1] for i in range(start_idx,end_idx)]
        # compute the cost of this part
        rse, parabola = polyfit(x, y, 2)

        # add the part temple to parabolas_and_x_range array 
        parabolas_and_x_range.append((parabola, points[start_idx][0], points[end_idx-1][0]))
        part_tample = (start_idx, end_idx, rse)
        sub_parts_tamples.append(part_tample)
        start_idx = end_idx
    
    opt_rse = 0
    # take the best parts - find the best in each iteretion and remove its from the tamples array
    for l in range(NUMBER_OF_BEST_PARTS_TAKEN):
        min_rse = float('inf')
        min_part_start_idx = 0
        min_part_end_idx = 0
        min_sub_part = None
        for sub_part in sub_parts_tamples: # find the best part and remove(make a hole in this place) it(so second best is now the best)
            rse = sub_part[2]
            if rse < min_rse: # check if part is "better" then the best so far
                min_sub_part = sub_part
                min_rse = rse
                min_part_start_idx = sub_part[0]
                min_part_end_idx = sub_part[1]
        
        opt_rse += min_rse
        sub_parts_tamples.remove(min_sub_part)
        
        # make a hole(infinity) in the place of the best part
        for i in range(min_part_start_idx, min_part_end_idx):
            points[i] = (float('inf'))
    
    # now remove all the holes so we stay without the best parts
    left_points = []
    for point in points:
        if point  != float('inf'):
            left_points.append(point)
    
    
    
    return opt_rse, left_points, parabolas_and_x_range


# compute the cost of set of points
# Time: O(n)
# Space: O(1)
def polyfit(x, y, deg):
    rse = 0
    coefficients = np.polyfit(x, y, deg)
    parabola = np.poly1d(coefficients)
    for i in range(len(x)):
        redusial = (parabola(x[i]) - y[i]) ** 2
        rse += redusial
    return rse, parabola
    


def test_optimal_bicriteria_points():
    if __name__ == '__main__':
                # aproximate parabolas that we make point around them
        parabola1 = np.poly1d([1, -16, 64])
        parabola2 = np.poly1d([1, -48, 576])
        parabola3 = np.poly1d([-1, 80, -1500])
        parabola4 = np.poly1d([-1, 118, -3390])
        
        points1 = []
        # make point around the parabols 
        x = np.linspace(0, 16, 200)
        points1.extend((x0, parabola1(x0) + random.randint(-10, 10)) for x0 in x)
        x = np.linspace(16, 32, 200)
        points1.extend((x0, parabola2(x0) + random.randint(-10, 10)) for x0 in x)
        x = np.linspace(32, 48, 200)
        points1.extend((x0, parabola3(x0) + random.randint(-10, 10)) for x0 in x)
        x = np.linspace(48, 64, 200)
        points1.extend((x0, parabola4(x0) + random.randint(-10, 10)) for x0 in x)
        
        
        
        # aproximate parabolas that we make point around them
        rectangle = [(0,0), (100,90)] # rectangle attached to points (0,0) and (20,25)
        p = (50, 45)  # Coordinates of point p within the rectangle
        angle_distance_arr = distances(rectangle, p)
        points = []
        for point in angle_distance_arr:
            if point[1] != float('inf'):
                points.append(point)
                
        k = 5
        optimal_bicriteria_points(points, k)

test_optimal_bicriteria_points()