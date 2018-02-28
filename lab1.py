import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import math
import random

# page 89 - triang


def srpoly(center_pt, min_rad, max_rad, min_step_angle, max_step_angle):
    poly = []
    angle = 0
    while angle < 2 * math.pi:
        d = min_rad + random.random() * (max_rad - min_rad)
        next_pt = center_pt + d * np.array([ math.cos(angle), math.sin(angle) ])
        angle += min_step_angle + random.random() * (max_step_angle - min_step_angle)
        poly.append(next_pt)

    first_point = poly[0]
    if random.random() >= 0.5:
        poly.reverse()
    poly.append(first_point)
    return np.array(poly)


def striang_signed(a, b, c):
    det = (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])
    return det / 2


def triang_center(a, b, c):
    return (a + b + c) / 3


def spoly(poly):
    square = 0
    center = np.array([0.0, 0.0])
    for i in range(1, len(poly)-1):
        striang = striang_signed(poly[0], poly[i], poly[i + 1])
        center += striang * triang_center(poly[0], poly[i], poly[i + 1])
        square += striang
    return abs(square), center / square


def dir_test(poly):
    square = 0
    for i in range(1, len(poly) - 1):
        square += striang_signed(poly[0], poly[i], poly[i + 1])
    return np.sign(square)

poly_points = srpoly(np.array([5, 7]), 1, 7, math.radians(10), math.radians(30))
square, center = spoly(poly_points)
dir = dir_test(poly_points)

print(square)
print(dir)

fig, ax = plt.subplots()

polygon = mpatches.Polygon(poly_points)
ax.add_patch(polygon)
ax.plot(*poly_points.transpose(), marker='o', color='r', ls='')
ax.plot(*center.transpose(), marker='o', color='y', ls='')
ax.plot(*np.array([5, 7]).transpose(), marker='o', color='b', ls='')

# fig.savefig("test.png")
plt.show()