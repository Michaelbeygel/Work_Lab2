import numpy as np
import random

# Define the position of point p within the rectangle

def f(rectangle, p, x):
    x0 = rectangle[0][0]
    y0 = rectangle[0][1]
    x1 = rectangle[1][0]
    y1 = rectangle[1][1]
    Xp = p[0]
    Yp = p[1]
    pi = np.pi
    a11 = np.arctan((y1-Yp)/(x1-Xp))
    a12 = np.arctan((Yp-y0)/(x1-Xp))
    a2 = np.arctan((x1-Xp)/(y1-Yp)) + np.arctan((Xp-x0)/(y1-Yp))
    a3 = np.arctan((y1-Xp)/(Xp-x0)) + np.arctan((Yp-y0)/(Xp-x0))
    a4 = np.arctan((Xp-x0)/(Yp-y0)) + np.arctan((x1-Xp)/(Yp-y0))

    angle_zone_2 = (a11, a11+a2)
    angle_zone_3 = (a11+a2, a11+a2+a3)
    angle_zone_4 = (a11+a2+a3, a11+a2+a3+a4)

    if(x >= angle_zone_2[0] and x <= angle_zone_2[1]):
        wall = y1 - Yp
        angle = abs(pi/2 - x)
    elif(x >= angle_zone_3[0] and x <= angle_zone_3[1]):
        wall = Xp - x0
        angle = abs(pi - x)
    elif(x >= angle_zone_4[0] and x <= angle_zone_4[1]):
        wall = Yp - y0
        angle = abs(3*pi/2 - x)
    elif(x >= 2*pi - a12):
        wall = x1-Xp
        angle = 2*pi - x
    else:
        wall = x1-Xp
        angle =  x   

    f = wall/np.cos(angle)
    return f


def distances(rectangle, point):
    # Generate a range of angles from -2π to 2π
    angles = np.linspace(0, 2 * np.pi, 360)
    # Calculate the corresponding values of f(x)
    distances = [f(rectangle, point, angle) for angle in angles]
    
    ## Create the plot
    #plt.figure(figsize=(8, 4))
    #plt.plot(angles, distances, '.', label=f'f(x) for point {point} and rectangle {rectangle}')
    #plt.xlabel('Angle (radians)')
    #plt.ylabel('Distance to Side of Rectangle')
    #plt.title('Distance of Point P from Rectangle Side at Different Angles')
    #plt.grid()
    #plt.legend()
    #
    ## Create the plot
    #squared_distances = [x**2 for x in distances]
    #plt.figure(figsize=(8, 4))
    #plt.plot(angles, squared_distances, '.', label=f'f(x) for point {point} and rectangle {rectangle}')
    #plt.xlabel('Angle (radians)')
    #plt.ylabel('Squared distances to Side of Rectangle')
    #plt.title('Squared distance of Point P from Rectangle Side at Different Angles')
    #plt.grid()
    #plt.legend()
    #
    #plt.show()
    angle_distance = []
    for i in range(360):
        angle = angles[i]
        distance = distances[i]
        if(260< i < 277):
            angle_distance.append((angle, float('inf')))
        else:
            angle_distance.append((angle, distance + random.randint(-3, 3)))
    return angle_distance



def rectangle_from_distances(p, distances):
    x = []
    y = []
    pX = p[0]
    pY = p[1]
    for distance in distances:
        if(distance[1] != float('inf')):
            x.append(pX + distance[1] * np.cos(distance[0]))
            y.append(pY + distance[1] * np.sin(distance[0]))
    
    return x, y