import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import math
import random
from matplotlib.widgets import Slider, Button

# page
# тест криволинейной фигурой эллипсом и ниже в главе
# есть функции более сложных фигур (page 59)
# ручной ввод полигона, случайный полигон
# 
# page 64
# сопряжение окружности: двигать прямую или окружность (или и то и то)
# проверять возможное отсутствие решений и вообще возможные решения
# т.е поверять возможно ли вписать дугу в область между прямой и окружностью


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


def ellipse(a, b, n=100):
    p_range = np.linspace(0, 2 * math.pi, num=n)
    ellipse_pts = []
    for p in p_range:
        ellipse_pts.append([
            a * math.cos(p),
            b * math.sin(p)
        ])
    return np.array(ellipse_pts)


def figure(n=100):
    fig_pts = []
    t_range = np.linspace(0, 2 * math.pi, num=n)
    for t in t_range:
        radius = 2 + math.cos(10.0 * t)
        angle = t + 0.5 * math.pow(math.sin(10.0 * t), 2)
        fig_pts.append([
            radius * math.cos(angle),
            radius * math.sin(angle)
        ])
    return np.array(fig_pts)


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


# PLOTTING

fig, ((ax_static_poly, ax_random_poly), (ax_ellipse, ax_figure)) = plt.subplots(2, 2,
                                                                                sharex=False, sharey=False,
                                                                                num=None, figsize=(10, 10), dpi=110
                                                                                )
fig.canvas.set_window_title('CG lab 1')


# STATIC POLYGON
static_polygon_points = np.array([
    [-3, 0],
    [0, 3],
    [3, 0],
    [0, -3],
])
static_poly_square, static_poly_center = spoly(static_polygon_points)
static_poly_dir = dir_test(static_polygon_points)
static_polygon_patch = mpatches.Polygon(static_polygon_points)
ax_static_poly.set_title('Manual')
ax_static_poly.set_xlabel('S={:.4f} dir={:.0f}'.format(static_poly_square, static_poly_dir))
ax_static_poly.set_aspect('equal')
ax_static_poly.add_patch(static_polygon_patch)
ax_static_poly.plot(*static_poly_center.transpose(), marker='o', color='r', ls='')


# RANDOM POLYGON
random_polygon_points = srpoly(np.array([0, 0]), 1, 7, math.radians(10), math.radians(30))
random_poly_square, random_poly_center = spoly(random_polygon_points)
random_poly_dir = dir_test(random_polygon_points)
random_polygon_patch = mpatches.Polygon(random_polygon_points)
ax_random_poly.set_title('Random polygon')
ax_random_poly.set_xlabel('S={:.4f} dir={:.0f}'.format(random_poly_square, random_poly_dir))
ax_random_poly.set_aspect('equal')
ax_random_poly.add_patch(random_polygon_patch)
lines_rpoly, = ax_random_poly.plot(*random_poly_center.transpose(), marker='o', color='r', ls='')

ax_next = plt.axes([0.3, 0.42, 0.2, 0.04])
bt_next = Button(ax_next, 'New random poly')


def update_poly(v):
    global random_polygon_patch, ax_random_poly, random_polygon_points, random_poly_square, random_poly_center, random_poly_dir
    random_polygon_points = srpoly(np.array([0, 0]), 1, 7, math.radians(10), math.radians(30))
    random_poly_square, random_poly_center = spoly(random_polygon_points)
    random_poly_dir = dir_test(random_polygon_points)
    random_polygon_patch.xy = random_polygon_points
    ax_random_poly.set_xlabel('S={:.4f} dir={:.0f}'.format(random_poly_square, random_poly_dir))
    lines_rpoly.set_data(*random_poly_center.transpose())
    print('Next')
    pass


bt_next.on_clicked(update_poly)

# ELLIPSE
ellipse_a = 7
ellipse_b = 3
ellipse_points = ellipse(ellipse_a, ellipse_b, n=1000)
ellipse_poly_square, ellipse_poly_center = spoly(ellipse_points)
ellipse_poly_dir = dir_test(ellipse_points)
ellipse_square = math.pi * ellipse_a * ellipse_b
ellipse_polygon_patch = mpatches.Polygon(ellipse_points)
ax_ellipse.set_title('Ellipse')
ax_ellipse.set_xlabel('S={:.4f} S\'={:.4f} dir={:.0f}'.format(ellipse_poly_square, ellipse_square, ellipse_poly_dir))
ax_ellipse.set_aspect('equal')
ax_ellipse.add_patch(ellipse_polygon_patch)
lines_ell, = ax_ellipse.plot(*ellipse_poly_center.transpose(), marker='o', color='r', ls='')

ax_ell_a = plt.axes([0.02, 0.05, 0.2, 0.04])
ax_ell_b = plt.axes([0.3, 0.05, 0.2, 0.04])

sl_ell_a = Slider(ax_ell_a, 'a', 1, 10, valinit=ellipse_a)
sl_ell_b = Slider(ax_ell_b, 'b', 1, 10, valinit=ellipse_b)


def update_ell(val):
    global ellipse_a, ellipse_b, ellipse_points, ellipse_polygon_patch, ellipse_poly_square, ellipse_poly_center, ax_ellipse, ellipse_square
    ellipse_a = sl_ell_a.val
    ellipse_b = sl_ell_b.val
    ellipse_points = ellipse(ellipse_a, ellipse_b, n=1000)
    ellipse_poly_square, ellipse_poly_center = spoly(ellipse_points)
    ellipse_square = math.pi * ellipse_a * ellipse_b
    ellipse_polygon_patch.xy = ellipse_points
    lines_ell.set_data(*ellipse_poly_center.transpose())
    ax_ellipse.set_xlabel('S={:.4f} S\'={:.4f} dir={:.0f}'.format(ellipse_poly_square, ellipse_square, ellipse_poly_dir))


sl_ell_a.on_changed(update_ell)
sl_ell_b.on_changed(update_ell)

# FIGURE
figure_polygon_points = figure(n=1000)
figure_poly_square, figure_poly_center = spoly(figure_polygon_points)
figure_poly_dir = dir_test(figure_polygon_points)
figure_polygon_patch = mpatches.Polygon(figure_polygon_points)
ax_figure.set_title('Figure')
ax_figure.set_xlabel('S={:.4f} dir={:.0f}'.format(figure_poly_square, figure_poly_dir))
ax_figure.set_aspect('equal')
ax_figure.add_patch(figure_polygon_patch)
ax_figure.plot(*figure_poly_center.transpose(), marker='o', color='r', ls='')


# Draw
fig.tight_layout()
plt.show()
