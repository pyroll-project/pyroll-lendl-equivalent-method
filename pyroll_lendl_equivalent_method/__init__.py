from pyroll import RollPass
from . import in_profile_hookspecs
from . import out_profile_hookspecs
from . import roll_pass_hookspecs

RollPass.plugin_manager.add_hookspecs(roll_pass_hookspecs)
RollPass.InProfile.plugin_manager.add_hookspecs(in_profile_hookspecs)
RollPass.OutProfile.plugin_manager.add_hookspecs(out_profile_hookspecs)
