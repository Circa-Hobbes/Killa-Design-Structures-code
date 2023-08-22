import sys

sys.path.append(
    "D:/OneDrive - Killa Design/Documents/GitHub/Killa-Design-Structures-code/V2_kld beam reinf code"
)

from beam_calculator_class import Beam


def test_get_long_count():
    test_beam = Beam(
        id=None,
        width=200,
        depth=None,
        pos_flex_combo=None,
        neg_flex_combo=None,
        req_top_flex_reinf=None,
        req_bot_flex_reinf=None,
        req_flex_torsion_reinf=None,
        shear_combo=None,
        torsion_combo=None,
        req_shear_reinf=None,
        req_torsion_reinf=None,
    )
    flex_count = test_beam.get_long_count()
    assert flex_count == 2


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
    # assert test_beam.side_face_middle_string == "T12@250 EF"
    # assert test_beam.side_face_right_string == "T12@250 EF"
