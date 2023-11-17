import logging
import webbrowser
from pathlib import Path

from pyroll.core import Profile, Roll, RollPass, Transport, RoundGroove, CircularOvalGroove, PassSequence, root_hooks
import pyroll.lendl_equivalent_method

root_hooks.add(Profile.equivalent_width)


def test_solve(tmp_path: Path, caplog):
    caplog.set_level(logging.INFO, logger="pyroll")

    def equivalent_width(self: RollPass.OutProfile):
        return 1.1 * self.roll_pass.in_profile.equivalent_width

    hf = RollPass.OutProfile.equivalent_width.add_function(equivalent_width)

    in_profile = Profile.round(
        diameter=30e-3,
        temperature=1200 + 273.15,
        strain=0,
        material=["C45", "steel"],
        flow_stress=100e6,
        length=1,
    )

    sequence = PassSequence([
        RollPass(
            label="Oval I",
            orientation="h",
            roll=Roll(
                groove=CircularOvalGroove(
                    depth=8e-3,
                    r1=6e-3,
                    r2=40e-3
                ),
                nominal_radius=160e-3,
                rotational_frequency=1
            ),
            gap=2e-3,
        ),
        Transport(
            label="I => II",
            duration=1
        ),
        RollPass(
            label="Round II",
            orientation="v",
            roll=Roll(
                groove=RoundGroove(
                    r1=1e-3,
                    r2=12.5e-3,
                    depth=11.5e-3
                ),
                nominal_radius=160e-3,
                rotational_frequency=1
            ),
            gap=2e-3,
        ),
        Transport(
            label="II => III",
            duration=1
        ),
        RollPass(
            label="Oval III",
            orientation="h",
            roll=Roll(
                groove=CircularOvalGroove(
                    depth=6e-3,
                    r1=6e-3,
                    r2=35e-3
                ),
                nominal_radius=160e-3,
                rotational_frequency=1
            ),
            gap=2e-3,
        ),
    ])

    try:
        sequence.solve(in_profile)
    finally:
        print("\nLog:")
        print(caplog.text)

        RollPass.OutProfile.equivalent_width.remove_function(hf)

    try:
        import pyroll.report

        report = pyroll.report.report(sequence)

        report_file = tmp_path / "report.html"
        report_file.write_text(report)
        print(report_file)
        webbrowser.open(report_file.as_uri())

    except ImportError:
        pass
