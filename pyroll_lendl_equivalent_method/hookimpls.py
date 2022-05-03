from pyroll import Profile, RollPass
from collections import namedtuple

from shapely import ops
from shapely.geometry import LineString
from shapely.affinity import rotate


@RollPass.hookimpl
def in_profile_groove_intersection_points(roll_pass: RollPass):
    in_profile_right_contour = rotate(roll_pass.in_profile.upper_contour_line, roll_pass.in_profile.rotation, (0, 0))
    in_profile_left_contour = rotate(roll_pass.in_profile.lower_contour_line, roll_pass.in_profile.rotation, (0, 0))

    right_intersection_points = in_profile_right_contour.intersection(roll_pass.groove.contour_line)
    left_intersection_points = in_profile_left_contour.intersection(roll_pass.groove.contour_line)

    intersection_points = ops.unary_union([right_intersection_points, left_intersection_points])

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
    initial_lendl_upper_contour = []
    initial_lendl_lower_contour = []

    for point in roll_pass.in_profile.upper_contour_line.coords:
        if roll_pass.upper_left_intersection_point.x < point[0] < roll_pass.upper_right_intersection_point.x:
            initial_lendl_upper_contour.append(point)

    for point in roll_pass.in_profile.lower_contour_line.coords:
        if roll_pass.lower_left_intersection_point.x < point[0] < roll_pass.lower_right_intersection_point.x:
            initial_lendl_lower_contour.append(point)

    initial_lendl_upper_contour = LineString(initial_lendl_upper_contour)
    initial_lendl_lower_contour = LineString(initial_lendl_lower_contour)
    initial_lendl_polygon = ops.unary_union([roll_pass.left_lendl_width_boundary,
                                             initial_lendl_upper_contour,
                                             initial_lendl_lower_contour,
                                             roll_pass.right_lendl_width_boundary]).convex_hull
    return initial_lendl_polygon.area


@RollPass.hookimpl
def lendl_final_area(roll_pass: RollPass):
    final_lendl_upper_contour = []
    final_lendl_lower_contour = []
    for point in roll_pass.in_profile.upper_contour_line.coords:
        if roll_pass.upper_left_intersection.x < point[0] < roll_pass.upper_right_intersection.x:
            final_lendl_upper_contour.append(point)

    for point in roll_pass.in_profile.lower_contour_line.coords:
        if roll_pass.lower_left_intersection.x < point[0] < roll_pass.lower_right_intersection.x:
            final_lendl_lower_contour.append(point)

    final_lendl_upper_contour = LineString(final_lendl_upper_contour)
    final_lendl_lower_contour = LineString(final_lendl_lower_contour)
    final_lendl_polygon = ops.unary_union([roll_pass.left_lendl_width_boundary,
                                           final_lendl_upper_contour,
                                           final_lendl_lower_contour,
                                           roll_pass.right_lendl_width_boundary]).convex_hull

    return final_lendl_polygon.area


@RollPass.InProfile.hookimpl(specname="equivalent_rectangle")
def in_equivalent_rectangle(roll_pass: RollPass, profile: Profile):
    eq_width = profile.width
    eq_height = roll_pass.lendl_initial_area / roll_pass.lendl_width

    Dimensions = namedtuple("Dimensions", ["width", "height"])

    return Dimensions(eq_width, eq_height)


@RollPass.OutProfile.hookimpl(specname="equivalent_rectangle")
def out_equivalent_rectangle(roll_pass: RollPass, profile: Profile):
    eq_width = profile.width
    eq_height = roll_pass.lendl_final_area / roll_pass.lendl_width

    Dimensions = namedtuple("Dimensions", ["width", "height"])

    return Dimensions(eq_width, eq_height)
