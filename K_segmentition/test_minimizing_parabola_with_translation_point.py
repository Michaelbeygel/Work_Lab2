import random
from matplotlib import pyplot as plt
import numpy as np
from numpy import RankWarning
from rectangle_problem.min_points import get_rectangle_coordinates, min_parabols
from path_algo.k_shortest_path_with_translation_point import k_shortest_path_with_translation_point
from path_algo.makeD_k import  makeD_k
from path_algo.makeD_asymetric import  makeD_asymetric
from path_algo.makeD import makeD
from rectangle_problem.point_in_rectangle import distances, rectangle_from_distances
from minimizing_parabola import best_k_parabols
from find_optimal_k import find_optimal_k
import warnings
# Filter out RankWarning
warnings.filterwarnings("ignore", category= RankWarning)

# test for best_k_parabols(P, D, k) function
def test_minimizing_parabola_with_translation_point():
    if __name__ == '__main__':
           
        rectangle = [(0,0), (100,90)] # rectangle attached to points (0,0) and (20,25)
        p = (50, 45)  # Coordinates of point p within the rectangle
        angle_distance_arr = distances(rectangle, p)
        exmples = [angle_distance_arr]
        
        # array of the number of parabols wwe ant for each exmple
        
        for e in range(len(exmples)):
            print(f'start computing exmple: {e+1}')
            #  set array of x coordinates and array of y coordinates
            x_coordinates_before_transletion = []
            y_coordinates_before_transletion = []
            
            # finding start & end of the hole
            i = 0
            while i < len(angle_distance_arr):
                if angle_distance_arr[i][1] != float('inf'):
                    x_coordinates_before_transletion.append(angle_distance_arr[i][0])
                    y_coordinates_before_transletion.append(angle_distance_arr[i][1])
                else:
                    # compute xy of hole with given point p, the angle and the distance from the rectangle in this directtion
                    x_hole = p[0] + angle_distance_arr[i-1][1] * np.cos(angle_distance_arr[i][0])
                    y_hole = p[1] + angle_distance_arr[i-1][1] * np.sin(angle_distance_arr[i][0])
                    start_hole = (x_hole, y_hole)
                    start_hole_angle = angle_distance_arr[i][0]
                    while angle_distance_arr[i][1] == float('inf'):
                        i += 1   
                    x_hole = p[0] + angle_distance_arr[i][1] * np.cos(angle_distance_arr[i-1][0])
                    y_hole = p[1] + angle_distance_arr[i][1] * np.sin(angle_distance_arr[i-1][0])
                    end_hole = (x_hole, y_hole)       
                    end_hole_angle = angle_distance_arr[i][0]     
                i += 1
                
            print(f"start hole: {start_hole} \n end hole: {end_hole}")
            print(start_hole_angle)
            print(end_hole_angle)
                        
            n = len(x_coordinates_before_transletion)
            
            print(f"number of points: {n}")
            
            k = 4
            # make asymetric distances metrix
            asymetricD = makeD_asymetric(x_coordinates_before_transletion, y_coordinates_before_transletion)
            # make D_k - [i][j] (i<j) cell is optimal way to get from node i to j with k steps
            D_k = makeD_k(asymetricD, k-1)
            # compute the transletion point
            transletion = k_shortest_path_with_translation_point(asymetricD, D_k, k)
            
            print(f"transletion point is: {transletion}")
            print(f"radian transletion point is: {2 * np.pi * transletion/n}")
            
            # switch the sides of the array according to the transletion point
            x_coordinates = [x_coordinates_before_transletion[i] - 2 * np.pi for i in range(transletion+1,n)]
            x_coordinates.extend(x_coordinates_before_transletion[0:transletion+1])
            #x_coordinates = x_coordinates_before_transletion[transletion+1:n]
            y_coordinates = y_coordinates_before_transletion[transletion+1:n]
            y_coordinates.extend(y_coordinates_before_transletion[0:transletion+1])
            # generate the D, P arrays with makeD function on the new array
            D,P = makeD(x_coordinates, y_coordinates)
            
            # finding the optimal k and return the parabolas, residuals, shortestPath for that k
            parabolas, residuals, shortestPath = best_k_parabols(P, D, k)
        
            
            for i in range(k):
                print(f"{i+1} Best-fit parabola: \n {parabolas[i]} \n")

            print(f"Minimized sum of squared residuals: {residuals}")
            print(f"indxes of parabolas: {shortestPath}")
            
            

            # now just draw graphs
            # orgenize the returned data so its can be ploted
            #
            #
            #
            #
            #
            #
            x = []
            y = []
            if k > 1:
                start_idx = 0
                start_angle = 0
                for i in range(k-1):
                    end_idx = shortestPath[i]
                    end_angle = 2* np.pi * (end_idx/360)
                    parabola_i_x = []
                    parabola_i_y = []
                    
                    # check if the hole is in ith prabola and make it
                    if start_angle <= start_hole_angle <= end_hole_angle <= end_angle:
                        half1 = np.linspace(x_coordinates[start_idx], start_hole_angle, 500)
                        y1 = parabolas[i](half1)  
                        half2 = np.linspace(end_hole_angle, x_coordinates[end_idx], 500)
                        y2 = parabolas[i](half2) 
                        gap_x = np.linspace(start_hole_angle, end_hole_angle, 10)  # Values for x between 5 and 10
                        gap_y = np.full_like(gap_x, np.nan)
                        parabola_i_x = np.concatenate((half1, gap_x, half2))
                        parabola_i_y = np.concatenate((y1, gap_y, y2))
                    else:
                        # create 1000 equally spaced points between the start of the parabola to end to draw the returned parbola more acurate
                        parabola_i_x = np.linspace(x_coordinates[start_idx], x_coordinates[end_idx], 1000)

                        # calculate the y value for each element of the x vector
                        parabola_i_y = parabolas[i](parabola_i_x)  
      
                    x.append(parabola_i_x)
                    y.append(parabola_i_y)
                    start_idx = end_idx+1
                    start_angle = 2* np.pi * (start_idx/360)
                    
                    
                # do over again for last parabola
                start_idx = shortestPath[k-2]+1
                start_angle = 2* np.pi * (start_idx/360)
                
                end_idx = n-1
                end_angle = 2* np.pi * (end_idx/360)
                parabola_i_x = []
                parabola_i_y = []
                
                # check if the hole is in last prabola and make it
                if start_angle <= start_hole_angle <= end_hole_angle <= end_angle:
                        half1 = np.linspace(x_coordinates[start_idx], start_hole_angle, 500)
                        y1 = parabolas[k-1](half1)  
                        half2 = np.linspace(end_hole_angle, x_coordinates[end_idx], 500)
                        y2 = parabolas[k-1](half2) 
                        gap_x = np.linspace(start_hole_angle, end_hole_angle, 10)  # Values for x between 5 and 10
                        gap_y = np.full_like(gap_x, np.nan)
                        parabola_i_x = np.concatenate((half1, gap_x, half2))
                        parabola_i_y = np.concatenate((y1, gap_y, y2))
                else:
                    parabola_i_x = np.linspace(x_coordinates[start_idx], x_coordinates[end_idx], 1000)
                    
                    parabola_i_y = parabolas[k-1](parabola_i_x) 



                x.append(parabola_i_x)
                y.append(parabola_i_y)
            else: # if k == 1
                parabola_0_x = np.linspace(x_coordinates[0], x_coordinates[n-1], 1000)
                parabola_0_y = parabolas[0](parabola_0_x) 
                x.append(parabola_0_x)
                y.append(parabola_0_y)
                
            # get xy coordinates of the rectangle using the distances signal and point p
            rectangleX, rectangleY = rectangle_from_distances(p, angle_distance_arr)
            
            # return n minimum points from n given parabolas
            min_points = min_parabols(parabolas)
            rectangle_shape = get_rectangle_coordinates(min_points, p)
             
            
            

            
            # generate the Plots
            plt.figure(f'before transletion')
            plt.plot(x_coordinates_before_transletion, y_coordinates_before_transletion, '.', color = 'black')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.legend()
            plt.title(f'before transletion')
            
            # generate  Plot after transletion
            plt.figure(f'k_parabolas after transletion')
            for i in range(k):
                plt.plot(x[i], y[i], label= f'{parabolas[i]}', )
            plt.plot(x_coordinates, y_coordinates, '.', color = 'black')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.legend()
            plt.title(f'k_parabolas after transletion')
            
            # drawing the rectangle
            plt.figure(f'rectangle xy coordinates')
            plt.plot(p[0], p[1], '.', color = 'red')
            x0 = rectangle_shape[0][0]
            y0 = rectangle_shape[0][1]
            x1 = rectangle_shape[1][0]
            y1 = rectangle_shape[1][1]
            plt.plot([end_hole[0], x1, x1, x0, x0, start_hole[0]], [y0, y0, y1, y1, y0, y0])
            plt.plot(rectangleX, rectangleY, '.', color = 'black')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.legend()
            plt.title(f'rectangle xy coordinates for rectangle: {rectangle} and point {p}')

            plt.show()  
            #
            #
            #
            #
            #
            #

test_minimizing_parabola_with_translation_point()
