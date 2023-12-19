def min_parabols(parabolas):
    min_points = []
    for parabola in parabolas:
        coefficients = parabola.coef
        x0 = -1 * coefficients[1] / (2 * coefficients[0])
        min_points.append((x0, parabola(x0)))
         
    return min_points

def get_rectangle_coordinates(min_points, p):
    x1 = p[0] + min_points[0][1]
    y1 = p[1] + min_points[1][1]
    x0 = p[0] - min_points[2][1]
    y0 = p[1] - min_points[3][1]
    return [(x0, y0), (x1, y1)]