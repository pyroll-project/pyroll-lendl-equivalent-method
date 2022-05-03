import math

import numpy as np
from shapely.ops import clip_by_rect

from pyroll import Profile, RollPass
from collections import namedtuple

from shapely import ops
from shapely.geometry import LineString
from shapely.affinity import rotate


@RollPass.hookimpl
def in_profile_groove_intersection_points(roll_pass: RollPass):
    in_profile_right_contour = rotate(roll_pass.in_profile.upper_contour_line, roll_pass.in_profile.rotation, (0, 0))
    in_profile_left_contour = rotate(roll_pass.in_profile.lower_contour_line, roll_pass.in_profile.rotation, (0, 0))

    intersection_points = ops.unary_union([
        in_profile_right_contour.intersection(roll_pass.upper_contour_line),
        in_profile_right_contour.intersection(roll_pass.lower_contour_line),
        in_profile_left_contour.intersection(roll_pass.upper_contour_line),
        in_profile_left_contour.intersection(roll_pass.lower_contour_line)
    ])

    return intersection_points


@RollPass.hookimpl
def upper_left_intersection_point(roll_pass: RollPass):
    upper_left_intersection = None
    for point in roll_pass.in_profile_groove_intersection_points.geoms:
        if point.x < 0 < point.y:
            upper_left_intersection = point

    return upper_left_intersection


@RollPass.hookimpl
def upper_right_intersection_point(roll_pass: RollPass):
    upper_right_intersection = None
    for point in roll_pass.in_profile_groove_intersection_points.geoms:
        if point.x > 0 and point.y > 0:
            upper_right_intersection = point

    return upper_right_intersection


@RollPass.hookimpl
def lower_right_intersection_point(roll_pass: RollPass):
    lower_right_intersection = None
    for point in roll_pass.in_profile_groove_intersection_points.geoms:
        if point.x > 0 > point.y:
            lower_right_intersection = point

    return lower_right_intersection


@RollPass.hookimpl
def lower_left_intersection_point(roll_pass: RollPass):
    lower_left_intersection = None
    for point in roll_pass.in_profile_groove_intersection_points.geoms:
        if point.x < 0 and point.y < 0:
            lower_left_intersection = point

    return lower_left_intersection


@RollPass.hookimpl
def left_lendl_width_boundary(roll_pass: RollPass):
    return LineString([roll_pass.upper_left_intersection_point, roll_pass.lower_left_intersection_point])


@RollPass.hookimpl
def right_lendl_width_boundary(roll_pass: RollPass):
    return LineString([roll_pass.upper_right_intersection_point, roll_pass.lower_right_intersection_point])


@RollPass.hookimpl
def lendl_width(roll_pass: RollPass):
    return roll_pass.left_lendl_width_boundary.distance(roll_pass.right_lendl_width_boundary)


@RollPass.hookimpl
def lendl_initial_area(roll_pass: RollPass):
    return clip_by_rect(
        roll_pass.in_profile.cross_section, -roll_pass.lendl_width / 2, -math.inf, roll_pass.lendl_width / 2,
        math.inf).area


@RollPass.hookimpl
def lendl_final_area(roll_pass: RollPass):
    return clip_by_rect(
        roll_pass.out_profile.cross_section, -roll_pass.lendl_width / 2, -math.inf, roll_pass.lendl_width / 2,
        math.inf).area


@RollPass.InProfile.hookimpl(specname="equivalent_rectangle")
def in_equivalent_rectangle(roll_pass: RollPass, profile: Profile):
    eq_width = profile.rotated.width
    eq_height = roll_pass.lendl_initial_area / roll_pass.lendl_width

    Dimensions = namedtuple("Dimensions", ["width", "height"])

    return Dimensions(eq_width, eq_height)


@RollPass.OutProfile.hookimpl(specname="equivalent_rectangle")
def out_equivalent_rectangle(roll_pass: RollPass, profile: Profile):
    eq_width = profile.width
    eq_height = roll_pass.lendl_final_area / roll_pass.lendl_width

    Dimensions = namedtuple("Dimensions", ["width", "height"])

    return Dimensions(eq_width, eq_height)
