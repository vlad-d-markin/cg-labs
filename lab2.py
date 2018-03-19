import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import math
from shapely.geometry import LineString, LinearRing, MultiLineString, Point

# page
# тест криволинейной фигурой эллипсом и ниже в главе
# есть функции более сложных фигур (page 59)
# ручной ввод полигона, случайный полигон
#
# page 64
# сопряжение окружности: двигать прямую или окружность (или и то и то)
# проверять возможное отсутствие решений и вообще возможные решения
# т.е поверять возможно ли вписать дугу в область между прямой и окружностью


def len_vec(vec):
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2)


def angle_vec(vec1, vec2):
    return math.acos(
        (vec1[0] * vec2[0] + vec1[1] * vec2[1])
        /
        (len_vec(vec1) * len_vec(vec2))
    )


def arc(center, radius, ang1, ang2, n=100):
    p_range = np.linspace(ang1, ang2, num=n)
    arc_pts = []
    for p in p_range:
        arc_pts.append([
            center[0] + radius * math.cos(p),
            center[1] + radius * math.sin(p)
        ])
    return np.array(arc_pts)


def circle(center, radius, n=100):
    p_range = np.linspace(0, 2 * math.pi, num=n)
    circle_pts = []
    for p in p_range:
        circle_pts.append([
            center[0] + radius * math.cos(p),
            center[1] + radius * math.sin(p)
        ])
    return np.array(circle_pts)


def line(A, B, min_X, max_X):
    pts = np.array([
        [min_X, (min_X * (A[1] - B[1]) + (A[0] * B[1] - B[0] * A[1])) / (A[0] - B[0])],
        [max_X, (max_X * (A[1] - B[1]) + (A[0] * B[1] - B[0] * A[1])) / (A[0] - B[0])]
    ])
    return pts


# PLOTTING
fig, ax = plt.subplots(figsize=(10, 10), dpi=110)
fig.canvas.set_window_title('CG lab 2')
plt.subplots_adjust(top=0.85, bottom=0.25)
plt.axis([-12, 12, -12, 12])

#ax = plt.axes([0, 0.25, 0.65, 1])

arc_R = 3

circle_R = 4
circle_center = np.array([0, 0])
circle_points = circle(circle_center, circle_R)
lines_circle, = ax.plot(*circle_points.transpose())
ax.set_aspect('equal')

ax_circleR = plt.axes([0.2, 0.9, 0.3, 0.04])
sl_circleR = Slider(ax_circleR, 'Circle R', 0.5, 10, valinit=circle_R)


ax_arcR = plt.axes([0.6, 0.9, 0.3, 0.04])
sl_arcR = Slider(ax_arcR, 'Arc R', 1, 10, valinit=arc_R)

shape_circle = LinearRing(circle(circle_center, circle_R - arc_R))
shape_circle_main = LinearRing(circle(circle_center, circle_R))

pt_A = np.array([0, 0])
pt_B = np.array([1, 1])
line_points = line(pt_A, pt_B, -12, 12)
lines_line, = ax.plot(*line_points.transpose())

ax_lineAx = plt.axes([0.2, 0.12, 0.3, 0.04])
ax_lineAy = plt.axes([0.2, 0.05, 0.3, 0.04])
ax_lineBx = plt.axes([0.6, 0.12, 0.3, 0.04])
ax_lineBy = plt.axes([0.6, 0.05, 0.3, 0.04])

sl_lineAx = Slider(ax_lineAx, 'Ax', -10, 10, valinit=pt_A[0])
sl_lineAy = Slider(ax_lineAy, 'Ay', -10, 10, valinit=pt_A[1])
sl_lineBx = Slider(ax_lineBx, 'Bx', -10, 10, valinit=pt_B[0])
sl_lineBy = Slider(ax_lineBy, 'By', -10, 10, valinit=pt_B[1])


shape_line = LineString(line_points)
shape_line_left = shape_line.parallel_offset(arc_R, 'left')
shape_line_right = shape_line.parallel_offset(arc_R, 'right')

lines_intersect, = ax.plot([], marker='o', color='r', ls='')


def build_arc(center, radius, pt1, pt2):
    sh_pt1 = Point(pt1)
    sh_pt2 = Point(pt2)
    dist = sh_pt1.distance(sh_pt2)
    sh_arc_circle = LinearRing(circle(center, radius))
    arc = sh_arc_circle.intersection(LinearRing(circle(pt1, dist)).intersection(LinearRing(circle(pt2, dist))))
    return np.array(arc.geoms[0].coords)


def update(v):
    global circle_points
    global circle_R, arc_R
    global line_points, shape_line_left, shape_line_right
    global pt_A, pt_B
    # Update arc radius
    arc_R = sl_arcR.val
    # Update circle
    circle_R = sl_circleR.val
    circle_points = circle(np.array([0, 0]), circle_R)
    lines_circle.set_data(*circle_points.transpose())
    fig.canvas.draw_idle()
    shape_circle.coords = circle(circle_center, circle_R - arc_R)
    shape_circle_main.coords = circle(circle_center, circle_R)
    # Update lines
    pt_A[0] = sl_lineAx.val
    pt_A[1] = sl_lineAy.val
    pt_B[0] = sl_lineBx.val
    pt_B[1] = sl_lineBy.val
    line_points = line(pt_A, pt_B, -12, 12)
    lines_line.set_data(*line_points.transpose())
    fig.canvas.draw_idle()
    shape_line.coords = line_points
    shape_line_left = shape_line.parallel_offset(arc_R, 'left')
    shape_line_right = shape_line.parallel_offset(arc_R, 'right')
    # Calculate intersections
    if arc_R >= circle_R:
        print("Impossible")
        lines_intersect.set_data([], [])
        return
    # d = shape_line.distance(Point(circle_center))
    # if d > circle_R - 2 * arc_R:
    #     print("Impossible 2")
    #     lines_intersect.set_data([], [])
    #     return
    intersection = list(shape_circle.intersection(MultiLineString([shape_line_left, shape_line_right])))
    inter_coords = []
    print("N of intersections {}".format(len(intersection)))
    for pt in intersection:
        arc_ctr = np.array(list(pt.coords)[0])
        arc_pts = arc(circle_center - arc_ctr, arc_R, angle_vec(arc_ctr, np.array([1, 0])), math.radians(-30), n=50)

        inter_coords = inter_coords + [arc_pts]
    if len(inter_coords):
        lines_intersect.set_data(*np.array(inter_coords).transpose())


sl_circleR.on_changed(update)
sl_arcR.on_changed(update)

sl_lineAx.on_changed(update)
sl_lineAy.on_changed(update)
sl_lineBx.on_changed(update)
sl_lineBy.on_changed(update)

plt.show()
