import sys

sys.path.append(
    "C:/Users/adnan.a/OneDrive - Killa Design/Documents/GitHub/Killa-Design-Structures-code/unit_testing"
)

from beam_calculator_class import Beam


def test_side_face_string():
    test_beam = Beam(
        id=None,
        width=900,
        depth=900,
        pos_flex_combo="True",
        neg_flex_combo="True",
        req_top_flex_reinf=[1000, 1000, 1000],
        req_bot_flex_reinf=[1000, 1000, 1000],
        req_flex_torsion_reinf=[0, 0, 0],
        shear_combo="False",
        torsion_combo="False",
        req_shear_reinf=[0, 0, 0],
        req_torsion_reinf=[0, 0, 0],
    )

    test_beam.get_long_count()

    # Split the torsion reinforcement to the top and bottom rebar if the depth <= 600mm.
    test_beam.flex_torsion_splitting()

    # Begin calculating the required top and bottom longitudinal reinforcement.
    test_beam.get_top_flex_rebar_string()
    test_beam.get_top_flex_rebar_area()

    test_beam.get_bot_flex_rebar_string()
    test_beam.get_bot_flex_rebar_area()

    # Calculate the residual rebar obtained from the provided against the required.
    test_beam.get_residual_rebar()

    # Calculate the allowable side face clear space in beams which have a depth greater than 600mm.
    test_beam.get_side_face_clear_space()

    test_beam.get_side_face_string()

    assert test_beam.flex_top_left_rebar_string == "Overstressed. Please re-assess"
