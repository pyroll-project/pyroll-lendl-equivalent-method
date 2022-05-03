from pyroll import RollPass


@RollPass.hookimpl
def in_profile_groove_intersection_points(roll_pass: RollPass):
    """Intersection points between the incoming profile and the groove"""


@RollPass.hookimpl
def upper_left_intersection_point(roll_pass: RollPass):
    """Upper left intersection point between incoming profile and groove"""


@RollPass.hookimpl
def upper_right_intersection_point(roll_pass: RollPass):
    """Upper right intersection point between incoming profile and groove"""


@RollPass.hookimpl
def lower_right_intersection_point(roll_pass: RollPass):
    """Lower right intersection point between incoming profile and groove"""


@RollPass.hookimpl
def lower_left_intersection_point(roll_pass: RollPass):
    """Lower left intersection point between incoming profile and groove"""


@RollPass.hookimpl
def left_lendl_width_boundary(roll_pass: RollPass):
    """Line between the left side intersection points"""


@RollPass.hookimpl
def right_lendl_width_boundary(roll_pass: RollPass):
    """Line between the right side intersection points"""

@RollPass.hookimpl
def lendl_width(roll_pass: RollPass):
    """Distance between left and right boundary"""


@RollPass.hookimpl
def lendl_initial_area(roll_pass: RollPass):
    """Initial Lendl area"""


@RollPass.hookimpl
def lendl_final_area(roll_pass: RollPass):
    """Final Lendl area"""
