from shapely.geometry import LineString, Point
import numpy as np
from shapely import ops
from matplotlib import pyplot
from pyroll.core.grooves import CircularOvalGroove, RoundGroove
from pyroll.core.profile.profile import Profile
from shapely.affinity import translate, rotate

gap = 0.5e-3
groove = RoundGroove(r1=2e-3, r2=15.8e-3 / 2, depth=7.65e-3)
in_profile = Profile(groove=CircularOvalGroove(depth=4.43e-3, r1=6e-3, r2=25.5e-3), height=10e-3, width=5e-3)

upper_groove_contour = translate(groove.contour_line, yoff=gap / 2)
lower_groove_contour = rotate(upper_groove_contour, angle=180, origin=(0, 0))

upper_intersections = in_profile.upper_contour_line.intersection(upper_groove_contour)
lower_intersections = in_profile.lower_contour_line.intersection(lower_groove_contour)

intersection_points = ops.unary_union([upper_intersections, lower_intersections])

for point in intersection_points.geoms:
    if point.x < 0 and point.y < 0:
        lower_left_intersection = point
    elif point.x < 0 < point.y:
        upper_left_intersection = point
    elif point.x > 0 and point.y > 0:
        upper_right_intersection = point
    else:
        lower_right_intersection = point

initial_lendl_upper_contour = []
initial_lendl_lower_contour = []
for point in upper_groove_contour.coords:
    if upper_left_intersection.x < point[0] < upper_right_intersection.x:
        initial_lendl_upper_contour.append(point)

for point in lower_groove_contour.coords:
    if lower_left_intersection.x < point[0] < lower_right_intersection.x:
        initial_lendl_lower_contour.append(point)

initial_lendl_upper_contour = LineString(initial_lendl_upper_contour)
initial_lendl_lower_contour = LineString(initial_lendl_lower_contour)

final_lendl_upper_contour = []
final_lendl_lower_contour = []
for point in in_profile.upper_contour_line.coords:
    if upper_left_intersection.x < point[0] < upper_right_intersection.x:
        final_lendl_upper_contour.append(point)

for point in in_profile.lower_contour_line.coords:
    if lower_left_intersection.x < point[0] < lower_right_intersection.x:
        final_lendl_lower_contour.append(point)

final_lendl_upper_contour = LineString(final_lendl_upper_contour)
final_lendl_lower_contour = LineString(final_lendl_lower_contour)

left_lendl_width_points = []
right_lendl_width_points = []

for point in intersection_points.geoms:
    if point.x < 0:
        left_lendl_width_points.append(point)
    else:
        right_lendl_width_points.append(point)

left_boundary = LineString(left_lendl_width_points)
right_boundary = LineString(right_lendl_width_points)

initial_lendl_polygon = ops.unary_union([left_boundary, initial_lendl_upper_contour, initial_lendl_lower_contour, right_boundary]).convex_hull
final_lendl_polygon = ops.unary_union([left_boundary, final_lendl_upper_contour, final_lendl_lower_contour, right_boundary]).convex_hull


def plot_point(ax, ob: Point, color='C0', alpha=0.5):
    x, y = ob.xy
    ax.scatter(x, y, color=color, alpha=alpha)


def plot_line(ax, ob, color='C0',  linewidth=3, alpha=0.5, label=''):
    x, y = ob.xy
    ax.plot(x, y, linewidth=linewidth, color=color, solid_capstyle='round', alpha=alpha, label=label)


def plot_polygon(ax, polygon, color="C1",  linewidth=3, alpha=0.5, label=''):
    x, y = polygon.exterior.xy
    ax.plot(x, y, linewidth=linewidth, color=color, solid_capstyle='round', alpha=alpha, label=label)


fig = pyplot.figure()
ax1: pyplot.Axes = fig.add_subplot()

ax1.set_aspect("equal")
plot_line(ax1, upper_groove_contour, alpha=0.5, color='C0', label='profile')
plot_line(ax1, lower_groove_contour, alpha=0.5, color='C0')
plot_line(ax1, in_profile.upper_contour_line, alpha=0.5, color='C1', label='groove')
plot_line(ax1, in_profile.lower_contour_line, alpha=0.5, color='C1')
for point in intersection_points.geoms:
    plot_point(ax1, point, alpha=0.5)
plot_line(ax1, left_boundary, color='C3')
plot_line(ax1, right_boundary, color='C3')
# plot_line(ax1, initial_lendl_upper_contour, color='C4', label="Initial Lendl")
# plot_line(ax1, initial_lendl_lower_contour, color='C4')
# plot_line(ax1, final_lendl_upper_contour, color='C5', label="Final Lendl")
# plot_line(ax1, final_lendl_lower_contour, color='C5')
plot_polygon(ax1, initial_lendl_polygon, color='C5', label='Initial lendl')
plot_polygon(ax1, final_lendl_polygon, color='C6', label='Final lendl')
# print(initial_lendl_polygon.area)
# print(final_lendl_polygon.area)
pyplot.legend()
pyplot.show()
