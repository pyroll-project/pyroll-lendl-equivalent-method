import numpy as np

from pyroll import Profile, RollPass
from collections import namedtuple

from shapely import ops

from shapely.geometry import LineString


@RollPass.hookimpl
def lendl_width(roll_pass: RollPass):
    upper_intersection_points = roll_pass.in_profile.upper_contour_line.intersection(roll_pass.groove.contour_line)
    lower_intersection_points = roll_pass.in_profile.lower_contour_line.intersection(roll_pass.groove.contour_line)

    intersection_points = ops.unary_union([upper_intersection_points, lower_intersection_points])

    left_lendl_width_points = []
    right_lendl_width_points = []

    for point in intersection_points.geoms:
        if point.x < 0:
            left_lendl_width_points.append(point)
        else:
            right_lendl_width_points.append(point)

    left_boundary = LineString(left_lendl_width_points)
    right_boundary = LineString(right_lendl_width_points)

    return left_boundary.distance(right_boundary)


@Profile.hookimpl
def equivalent_rectangle(profile: Profile):
    width = profile.rotated.width
    height = profile.rotated.height

    eq_width = np.sqrt(profile.cross_section.area * width / height)
    eq_height = np.sqrt(profile.cross_section.area * height / width)

    Dimensions = namedtuple("Dimensions", ["width", "height"])

    return Dimensions(eq_width, eq_height)
