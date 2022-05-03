import math

from shapely.geometry import LineString
from shapely.affinity import rotate
from shapely.ops import clip_by_rect

from pyroll import Profile, RollPass
from pyroll.core.dimensions import Dimensions


@RollPass.InProfile.hookimpl
def right_contour(roll_pass: RollPass, profile: Profile):
    return rotate(roll_pass.in_profile.lower_contour_line, roll_pass.in_profile.rotation, (0, 0))


@RollPass.InProfile.hookimpl
def left_contour(roll_pass: RollPass, profile: Profile):
    return rotate(roll_pass.in_profile.upper_contour_line, roll_pass.in_profile.rotation, (0, 0))


@RollPass.hookimpl
def upper_left_intersection_point(roll_pass: RollPass):
    return roll_pass.in_profile.left_contour.intersection(roll_pass.upper_contour_line)


@RollPass.hookimpl
def upper_right_intersection_point(roll_pass: RollPass):
    return roll_pass.in_profile.right_contour.intersection(roll_pass.upper_contour_line)


@RollPass.hookimpl
def lower_right_intersection_point(roll_pass: RollPass):
    return roll_pass.in_profile.right_contour.intersection(roll_pass.lower_contour_line)


@RollPass.hookimpl
def lower_left_intersection_point(roll_pass: RollPass):
    return roll_pass.in_profile.left_contour.intersection(roll_pass.lower_contour_line)


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
        roll_pass.in_profile.cross_section, -roll_pass.lendl_width / 2,
        -math.inf, roll_pass.lendl_width / 2, math.inf).area


@RollPass.hookimpl
def lendl_final_area(roll_pass: RollPass):
    return clip_by_rect(
        roll_pass.out_profile.cross_section, -roll_pass.lendl_width / 2,
        -math.inf, roll_pass.lendl_width / 2, math.inf).area


@RollPass.InProfile.hookimpl(specname="equivalent_rectangle")
def in_equivalent_rectangle(roll_pass: RollPass, profile: Profile):
    eq_width = profile.rotated.width
    eq_height = roll_pass.lendl_initial_area / roll_pass.lendl_width

    return Dimensions(eq_width, eq_height)


@RollPass.OutProfile.hookimpl(specname="equivalent_rectangle")
def out_equivalent_rectangle(roll_pass: RollPass, profile: Profile):
    eq_width = profile.width
    eq_height = roll_pass.lendl_final_area / roll_pass.lendl_width

    return Dimensions(eq_width, eq_height)
