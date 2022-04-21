import numpy as np

from pyroll import Profile, RollPass, RollPassOutProfile, RollPassInProfile
from collections import namedtuple

from shapely import ops

from shapely.geometry import LineString, Polygon


@RollPass.hookimpl
def in_profile_groove_intersection_points(roll_pass: RollPass):
    upper_intersection_points = roll_pass.in_profile.upper_contour_line.intersection(roll_pass.groove.contour_line)
    lower_intersection_points = roll_pass.in_profile.lower_contour_line.intersection(roll_pass.groove.contour_line)

    intersection_points = ops.unary_union([upper_intersection_points, lower_intersection_points])

    return intersection_points


@RollPass.hookimpl
def left_lendl_width_boundary(roll_pass: RollPass):
    left_lendl_width_points = []

    for point in roll_pass.in_profile_groove_intersection_points.geoms:
        if point.x < 0:
            left_lendl_width_points.append(point)

    left_boundary = LineString(left_lendl_width_points)

    return left_boundary


@RollPass.hookimpl
def right_lendl_width_boundary(roll_pass: RollPass):
    right_lendl_width_points = []

    for point in roll_pass.in_profile_groove_intersection_points.geoms:
        if point.x > 0:
            right_lendl_width_points.append(point)

    right_boundary = LineString(right_lendl_width_points)

    return right_boundary


@RollPass.hookimpl
def lendl_width(roll_pass: RollPass):
    return roll_pass.left_lendl_width_boundary.distance(roll_pass.right_lendl_width_boundary)


@RollPassInProfile.hookimpl
def lendl_in_profile_area(roll_pass: RollPass):
    area_as_multi_line = ops.unary_union([roll_pass.left_lendl_width_boundary,
                                          roll_pass.right_lendl_width_boundary,
                                          roll_pass.groove.contour_line])

    merged_line = ops.linemerge(area_as_multi_line)
    area_as_polygon = Polygon(merged_line)
    return area_as_polygon.area


@RollPassOutProfile.hookimpl
def lendl_out_profile_area():
    pass


@Profile.hookimpl
def equivalent_rectangle(profile: Profile):
    width = profile.rotated.width
    height = profile.rotated.height

    eq_width = np.sqrt(profile.cross_section.area * width / height)
    eq_height = np.sqrt(profile.cross_section.area * height / width)

    Dimensions = namedtuple("Dimensions", ["width", "height"])

    return Dimensions(eq_width, eq_height)
