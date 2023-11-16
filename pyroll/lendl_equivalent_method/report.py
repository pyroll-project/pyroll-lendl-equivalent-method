from matplotlib import pyplot as plt
from pyroll.report import hookimpl
from pyroll.core import RollPass, Unit
from shapely import MultiLineString
from shapely.affinity import rotate
from typing import Union


@hookimpl
def unit_plot(unit: Unit):
    """Plot roll pass contour and its profiles"""
    if isinstance(unit, RollPass):
        fig: plt.Figure = plt.figure(constrained_layout=True, figsize=(4, 4))
        ax: plt.Axes = fig.subplots()

        ax.set_aspect("equal", "datalim")
        ax.grid(lw=0.5)
        plt.title("Lendl Areas and Boundaries")

        ax.fill(*unit.in_profile.lendl_section.boundary.xy, color="red", alpha=0.5)
        ax.fill(*unit.out_profile.lendl_section.boundary.xy, color="blue", alpha=0.5)

        def orient_contour_lines(contour_lines: MultiLineString):

            orientation = unit.orientation

            if isinstance(orientation, str):
                if orientation.lower() in ["horizontal", "h"]:
                    orientation = (0, 0)
                elif orientation.lower() in ["vertical", "v"]:
                    orientation = (90, 90)
                elif orientation.lower() in ["y"]:
                    orientation = (0, 0, 0)
                elif orientation.lower() in ["antiy", "ay"]:
                    orientation = (60, 180, 300)

            if isinstance(orientation, Union[int, float]):
                number_of_contour_lines = len(contour_lines)
                o = [orientation] * number_of_contour_lines
                return [rotate(cl, angle=a, origin=(0, 0)) for cl, a in zip(contour_lines, o)]

            return [rotate(cl, angle=a, origin=(0, 0)) for cl, a in zip(contour_lines, orientation)]

        contour_line_oriented = orient_contour_lines(unit.contour_lines)

        for cl in contour_line_oriented:
            ax.plot(*cl.xy, color="k")

        return fig
