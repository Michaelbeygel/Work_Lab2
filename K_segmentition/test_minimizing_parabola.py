import random
from matplotlib import pyplot as plt
import numpy as np
from numpy import RankWarning
from path_algo.makeD import makeD
from rectangle_problem.point_in_rectangle import distances
from minimizing_parabola import best_k_parabols
from find_optimal_k import find_optimal_k
import warnings
# Filter out RankWarning
warnings.filterwarnings("ignore", category= RankWarning)

# test for best_k_parabols(P, D, k) function
def test_minimizing_parabola():
    if __name__ == '__main__':
        
        # aproximate parabolas that we make point around them
        parabola1 = np.poly1d([1, -16, 64])
        parabola2 = np.poly1d([1, -48, 576])
        parabola3 = np.poly1d([-1, 80, -1500])
        parabola4 = np.poly1d([-1, 118, -3390])
        
        points1 = [(-16, 75), (-8,0), (-1, 75)]
        # make point around the parabols 
        x = np.linspace(0, 16, 200)
        points1.extend((x0, parabola1(x0) + random.randint(-10, 10)) for x0 in x)
        #x = np.linspace(16, 32, 200)
        #points1.extend((x0, parabola2(x0) + random.randint(-10, 10)) for x0 in x)
        points1.extend([(16, 140), (24,40), (32, 140)]) 
        x = np.linspace(32, 48, 200)
        points1.extend((x0, parabola3(x0) + random.randint(-10, 10)) for x0 in x)
        x = np.linspace(48, 64, 200)
        points1.extend((x0, parabola4(x0) + random.randint(-10, 10)) for x0 in x)
        
        #exmple 2
        points2 = [(0,9), (1,0), (2,9)]
        
        exmples = [points1]
        
        #exmples.extend(points2)
        
        p = (10, 10)  # Coordinates of point p within the rectangle
        rectangle = [(0,0), (20,25)] # rectangle attached to points (0,0) and (20,25)
        last_exmple = distances(rectangle, p)
        #exmples.append(last_exmple)
        
        # array of the number of parabols wwe ant for each exmple
        
        for e in range(len(exmples)):
            print(f'start computing exmple: {e+1}')
            #  set array of x coordinates and array of y coordinates
            points = exmples[e]
            x_coordinates = [point[0] for point in points]
            y_coordinates = [point[1] for point in points]
            
            n = len(points)

            # generate the D, P arrays with makeD function
            D,P = makeD(points)
            
            # finding the optimal k and return the parabolas, residuals, shortestPath for that k
                
            parabolas, residuals, shortestPath, k = find_optimal_k(D, P)
            
            for i in range(k):
                print(f"{i+1} Best-fit parabola: \n {parabolas[i]} \n")

            print(f"Minimized sum of squared residuals: {residuals}")
            print(f"indxes of parabolas: {shortestPath}")


            # orgenize the returned data so its can be ploted
            x = []
            y = []
            if k > 1:
                start_idx = 0

                for i in range(k-1):
                    end_idx = shortestPath[i]
                    parabola_i_x = []
                    parabola_i_y = []
                    # create 1000 equally spaced points between the start of the parabola to end to draw the returned parbola more acurate
                    parabola_i_x = np.linspace(x_coordinates[start_idx], x_coordinates[end_idx], 1000)

                    # calculate the y value for each element of the x vector
                    parabola_i_y = parabolas[i](parabola_i_x)  
                    
                    x.append(parabola_i_x)
                    y.append(parabola_i_y)
                    start_idx = end_idx+1
                    
                    
                # do over again for last parabola
                start_idx = shortestPath[k-2]+1
                end_idx = n-1
                parabola_i_x = []
                parabola_i_y = []
                
                parabola_i_x = np.linspace(x_coordinates[start_idx], x_coordinates[end_idx], 1000)
                parabola_i_y = parabolas[k-1](parabola_i_x) 

                x.append(parabola_i_x)
                y.append(parabola_i_y)
            else:
                parabola_0_x = np.linspace(x_coordinates[0], x_coordinates[n-1], 1000)
                parabola_0_y = parabolas[0](parabola_0_x) 
                x.append(parabola_0_x)
                y.append(parabola_0_y)



            # generate the Plots
            plt.figure(f'k_parabolas exmple {e + 1}')
            for i in range(k):
                plt.plot(x[i], y[i], label= f'{parabolas[i]}', )
            plt.plot(x_coordinates, y_coordinates, '.', color = 'black')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.legend()
            plt.title(f'{k} parabolas')
            
        plt.show()  
            

test_minimizing_parabola()