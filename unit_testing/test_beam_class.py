import sys

sys.path.append(
    r"C:/Users/adnan.a/OneDrive - Killa Design/Documents/GitHub/Killa-Design-Structures-code/unit_testing"
)
sys.path.append(
    r"C:\Users\adnan.a\OneDrive - Killa Design\Documents\GitHub\Killa-Design-Structures-code\V2_kld beam reinf code"
)

from beam_calculator_class import Beam


def test_side_face_string():
    """Note: for attributes with lists, index 0 is left, index 1 is middle, and index 2 is right."""
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

    # Get the effective depth by multiplying the depth by 0.8.
    test_beam.get_eff_depth()
    # Get the longitudinal rebar count.
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

    # Calculate the required shear legs based on the beams width.
    test_beam.get_shear_legs()

    # Calculate the total required shear reinforcement including shear and torsion.
    test_beam.get_total_shear_req()

    # Calculate the provided shear reinforcement string and area.
    test_beam.get_shear_string()
    test_beam.get_shear_area()

    # Check and replace if necessary the maximum longitudinal shear spacing against Clause 18.4.2.4 of ACI 318-19.
    test_beam.get_min_shear_long_spacing()
    test_beam.modify_shear_reinf()

    # Grab the index of the shear reinforcement with the highest area.
    # beam.get_index_for_shear_reinf()

    # Calculate the allowable side face clear space in beams which have a depth greater than 600mm.
    test_beam.get_side_face_clear_space()

    # Calculate the provided side face reinforcement string and area.
    test_beam.get_side_face_string()
    test_beam.get_side_face_area()

    # Grab the index of the side face reinforcement with the highest area.
    test_beam.get_index_for_side_face_reinf()

    assert test_beam.flex_top_left_rebar_string == "Overstressed. Please re-assess"
