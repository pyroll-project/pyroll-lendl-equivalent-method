from pyroll import RollPass


@RollPass.InProfile.hookspec
def equivalent_rectangle(roll_pass, profile):
    """Get the dimensions of the equivalent rectangle of the rotated profile."""
