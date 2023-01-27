import math

from pyroll.core import RollPass, Hook, ThreeRollPass
from shapely import intersection, MultiLineString, Polygon
from shapely.ops import clip_by_rect
import numpy as np

RollPass.lendl_width = Hook[float]()
RollPass.Profile.lendl_section = Hook[float]()


@RollPass.OutProfile.lendl_section
def out_lendl_section(self: RollPass.OutProfile):
    contour = MultiLineString(self.roll_pass.contour_lines)
    intersections = intersection(self.roll_pass.in_profile.cross_section, contour)

    return Polygon(
        np.concatenate([ls.coords for ls in intersections])
    )


@RollPass.lendl_width
def lendl_width(self: RollPass):
    return self.out_profile.lendl_section.width


@RollPass.InProfile.lendl_section
def in_lendl_section(self: RollPass.InProfile):
    half_width = self.roll_pass.lendl_width / 2
    return clip_by_rect(self.cross_section, -half_width, -math.inf, half_width, math.inf)


@RollPass.Profile.equivalent_width
def equivalent_width(self: RollPass.Profile):
    return self.roll_pass.lendl_width


@RollPass.Profile.equivalent_height
def equivalent_height(self: RollPass.Profile):
    return self.lendl_section.area / self.equivalent_width
