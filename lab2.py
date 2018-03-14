import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import math
import random

# page
# тест криволинейной фигурой эллипсом и ниже в главе
# есть функции более сложных фигур (page 59)
# ручной ввод полигона, случайный полигон
#
# page 64
# сопряжение окружности: двигать прямую или окружность (или и то и то)
# проверять возможное отсутствие решений и вообще возможные решения
# т.е поверять возможно ли вписать дугу в область между прямой и окружностью


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

circle_R = 4
circle_points = circle(np.array([0, 0]), circle_R)
lines_circle, = ax.plot(*circle_points.transpose())
ax.set_aspect('equal')

ax_circleR = plt.axes([0.2, 0.9, 0.3, 0.04])
sl_circleR = Slider(ax_circleR, 'Circle R', 0.5, 10, valinit=circle_R)


ax_arcR = plt.axes([0.6, 0.9, 0.3, 0.04])
sl_arcR = Slider(ax_arcR, 'Arc R', 1, 10)


def update_c(v):
    global circle_points
    global circle_R
    circle_R = sl_circleR.val
    circle_points = circle(np.array([0, 0]), circle_R)
    lines_circle.set_data(*circle_points.transpose())
    fig.canvas.draw_idle()


sl_circleR.on_changed(update_c)


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


def update_l(v):
    global line_points
    global pt_A, pt_B
    pt_A[0] = sl_lineAx.val
    pt_A[1] = sl_lineAy.val
    pt_B[0] = sl_lineBx.val
    pt_B[1] = sl_lineBy.val
    line_points = line(pt_A, pt_B, -12, 12)
    lines_line.set_data(*line_points.transpose())
    fig.canvas.draw_idle()


sl_lineAx.on_changed(update_l)
sl_lineAy.on_changed(update_l)
sl_lineBx.on_changed(update_l)
sl_lineBy.on_changed(update_l)

plt.show()
