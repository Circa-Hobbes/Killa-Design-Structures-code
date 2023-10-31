import pytest
from beamscheduler.beam_calculator_class import Beam
from pytest import approx


@pytest.fixture
def example_beam() -> Beam:
    """This example beam is utilised for testing purposes.
    Please define the attributes of the example beam in the following instance.

    This beam is currently mimicking beam B213 at P2, Revit ID: L2-B33.
    Returns:
        object: example beam to utilise in tests.
    """
    example_beam = Beam(
        id=None,
        width=600,
        depth=600,
        pos_flex_combo="False",
        neg_flex_combo="False",
        req_top_flex_reinf=[1553, 1083, 1648],
        req_bot_flex_reinf=[1083, 1325, 1083],
        req_flex_torsion_reinf=[1913, 1913, 1913],
        shear_combo="False",
        torsion_combo="False",
        req_shear_reinf=[605.91, 277.58, 605.91],
        req_torsion_reinf=[518.34, 214.48, 587.29],
    )
    return example_beam


def test_eff_depth(example_beam: Beam):
    """This test checks if the effective depth method obtains the correct value.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_eff_depth()
    assert example_beam.eff_depth == 0.8 * example_beam.depth


def test_get_long_count(example_beam: Beam):
    """This test checks if the get long count method obtains the correct value.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_long_count()
    assert example_beam.flex_rebar_count == 5


def test_get_flex_top_req(example_beam: Beam):
    """This test checks if the correct flexural reinforcement values are obtained.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.flex_torsion_splitting()
    assert example_beam.req_top_flex_reinf == [
        2509.5,
        2039.5,
        2604.5,
    ] and example_beam.req_flex_torsion_reinf == [0, 0, 0]


def test_get_flex_bot_req(example_beam: Beam):
    """This test checks if the correct flexural reinforcement values are obtained.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.flex_torsion_splitting()
    assert example_beam.req_bot_flex_reinf == [
        2039.5,
        2281.5,
        2039.5,
    ] and example_beam.req_flex_torsion_reinf == [0, 0, 0]


def test_top_flex_rebar_string(example_beam: Beam):
    """This test checks that the top flexural rebar matches what would be expected for
    the required area of steel.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_long_count()
    example_beam.flex_torsion_splitting()
    example_beam.get_top_flex_rebar_string()
    assert example_beam.flex_top_left_rebar_string == "5T20 + 5T16"
    assert example_beam.flex_top_middle_rebar_string == "5T20 + 5T16"
    assert example_beam.flex_top_right_rebar_string == "5T20 + 5T16"


def test_bot_flex_rebar_string(example_beam: Beam):
    """This test checks that the bottom flexural rebar matches what would be expected for
    the required area of steel.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_long_count()
    example_beam.flex_torsion_splitting()
    example_beam.get_bot_flex_rebar_string()
    assert example_beam.flex_bot_left_rebar_string == "5T20 + 5T16"
    assert example_beam.flex_bot_middle_rebar_string == "5T20"
    assert example_beam.flex_bot_right_rebar_string == "5T20 + 5T16"


def test_top_flex_rebar_area(example_beam: Beam):
    """This test checks that the top flexural rebar matches what would be expected for
    the required area of steel.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_long_count()
    example_beam.flex_torsion_splitting()
    example_beam.get_top_flex_rebar_area()
    assert example_beam.flex_top_left_rebar_area > 2509.5  # type: ignore
    assert example_beam.flex_top_middle_rebar_area > 2039.5  # type: ignore
    assert example_beam.flex_top_right_rebar_area > 2604.5  # type: ignore


def test_bot_flex_rebar_area(example_beam: Beam):
    """This test checks that the bottom flexural rebar matches what would be expected for
    the required area of steel.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_long_count()
    example_beam.flex_torsion_splitting()
    example_beam.get_bot_flex_rebar_area()
    assert example_beam.flex_bot_left_rebar_area > 2039.5  # type: ignore
    assert example_beam.flex_bot_middle_rebar_area > 2281.5  # type: ignore
    assert example_beam.flex_bot_right_rebar_area > 2039.5  # type: ignore


def test_residual_rebar(example_beam: Beam):
    """This test checks that the residual rebar value is correctly obtained

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_long_count()
    example_beam.flex_torsion_splitting()
    example_beam.get_top_flex_rebar_area()
    example_beam.get_bot_flex_rebar_area()
    example_beam.get_residual_rebar()
    assert example_beam.left_residual_rebar == (example_beam.flex_top_left_rebar_area - 2509.5) + (example_beam.flex_bot_left_rebar_area - 2039.5)  # type: ignore
    assert example_beam.middle_residual_rebar == (example_beam.flex_top_middle_rebar_area - 2039.5) + (example_beam.flex_bot_middle_rebar_area - 2281.5)  # type: ignore
    assert example_beam.right_residual_rebar == (example_beam.flex_top_right_rebar_area - 2604.5) + (example_beam.flex_bot_right_rebar_area - 2039.5)  # type: ignore


def test_total_shear_req(example_beam: Beam):
    """This test checks that the total shear requirement is correctly calculated.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_total_shear_req()
    assert example_beam.req_total_left_shear_reinf == 1642.5900000000001
    assert example_beam.req_total_middle_shear_reinf == 706.54
    assert example_beam.req_total_right_shear_reinf == 1780.4899999999998


def test_shear_legs(example_beam: Beam):
    """This test checks that the required shear legs is correctly obtained.
    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_shear_legs()
    assert example_beam.req_shear_legs == 4


def test_get_shear_string(example_beam: Beam):
    """This test checks that the obtained shear string is what is expected prior to checking the
    minimum spacing and filtering.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_total_shear_req()
    example_beam.get_shear_legs()
    example_beam.get_shear_string()
    assert example_beam.shear_left_string == "4L-T12@250"
    assert example_beam.shear_middle_string == "4L-T12@250"
    assert example_beam.shear_right_string == "4L-T12@250"


def test_shear_area(example_beam: Beam):
    """This test checks that the obtained shear area is what is expected prior to checking
    the minimum spacing and filtering.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_total_shear_req()
    example_beam.get_shear_legs()
    example_beam.get_shear_area()
    assert example_beam.shear_left_area == approx(1809.56, 2)
    assert example_beam.shear_middle_area == approx(1809.56, 2)
    assert example_beam.shear_right_area == approx(1809.56, 2)


def test_side_face_clear_space(example_beam: Beam):
    """This tests check that the obtained side face clear space is what is expected prior to
    calculating the side face string and area.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_long_count()
    example_beam.flex_torsion_splitting()
    example_beam.get_top_flex_rebar_string()
    example_beam.get_bot_flex_rebar_string()
    example_beam.get_total_shear_req()
    example_beam.get_shear_legs()
    example_beam.get_shear_string()
    example_beam.get_side_face_clear_space()
    assert example_beam.side_face_clear_space == "Not needed"


def test_side_face_string(example_beam: Beam):
    """This test checks that the obtained side face string is what is expected.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_long_count()
    example_beam.flex_torsion_splitting()
    example_beam.get_top_flex_rebar_string()
    example_beam.get_bot_flex_rebar_string()
    example_beam.get_total_shear_req()
    example_beam.get_shear_legs()
    example_beam.get_shear_string()
    example_beam.get_side_face_clear_space()
    example_beam.get_side_face_string()
    assert example_beam.side_face_left_string == "Not needed"
    assert example_beam.side_face_middle_string == "Not needed"
    assert example_beam.side_face_right_string == "Not needed"


def test_side_face_area(example_beam: Beam):
    """This test checks that the obtained side face area is what is expected.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_long_count()
    example_beam.flex_torsion_splitting()
    example_beam.get_top_flex_rebar_string()
    example_beam.get_bot_flex_rebar_string()
    example_beam.get_total_shear_req()
    example_beam.get_shear_legs()
    example_beam.get_shear_string()
    example_beam.get_side_face_clear_space()
    example_beam.get_side_face_area()

    assert example_beam.side_face_left_area == "Not needed"
    assert example_beam.side_face_middle_area == "Not needed"
    assert example_beam.side_face_right_area == "Not needed"


def test_index_for_side_face_reinf(example_beam: Beam):
    """This test checks that the index grabbed by the method is what is expected
    (grabbing the side face reinforcement with the highest area).

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_long_count()
    example_beam.flex_torsion_splitting()
    example_beam.get_top_flex_rebar_string()
    example_beam.get_bot_flex_rebar_string()
    example_beam.get_total_shear_req()
    example_beam.get_shear_legs()
    example_beam.get_shear_string()
    example_beam.get_side_face_clear_space()
    example_beam.get_side_face_area()
    example_beam.get_index_for_side_face_reinf()
    assert (
        example_beam.selected_side_face_reinforcement_string == "Not needed"
        and example_beam.selected_side_face_reinforcement_area == 0
    )


def test_index_for_shear_reinf(example_beam: Beam):
    """This test checks that the correct shear index is selected. e.g., the left and right should be max.
    If the middle is the max, then the left and right are set to that.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_total_shear_req()
    example_beam.get_shear_legs()
    example_beam.get_shear_string()
    example_beam.get_shear_area()
    example_beam.get_index_for_shear_reinf()
    assert example_beam.selected_shear_left_string == "4L-T12@250"
    assert example_beam.selected_shear_middle_string == "4L-T12@250"
    assert example_beam.selected_shear_right_string == "4L-T12@250"


def test_min_shear_long_spacing(example_beam: Beam):
    """This test checks that the smallest longitudinal spacing of the shear reinforcement is being
    accurately calculated.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_eff_depth()
    example_beam.get_long_count()
    example_beam.flex_torsion_splitting()
    example_beam.get_top_flex_rebar_string()
    example_beam.get_bot_flex_rebar_string()
    example_beam.get_total_shear_req()
    example_beam.get_shear_legs()
    example_beam.get_shear_string()
    example_beam.get_shear_area()
    example_beam.get_min_shear_long_spacing()
    assert example_beam.min_shear_long_spacing == 100
    assert example_beam.min_shear_centre_long_spacing == 200


def test_modified_shear_reinf(example_beam: Beam):
    """This test checks that the left and right shear reinforcement is being modified based on the minimum longitudinal
    shear spacing.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_eff_depth()
    example_beam.get_long_count()
    example_beam.flex_torsion_splitting()
    example_beam.get_top_flex_rebar_string()
    example_beam.get_bot_flex_rebar_string()
    example_beam.get_total_shear_req()
    example_beam.get_shear_legs()
    example_beam.get_shear_string()
    example_beam.get_shear_area()
    example_beam.get_min_shear_long_spacing()
    example_beam.modify_shear_reinf()
    assert example_beam.shear_left_string == "4L-T12@100"
    assert example_beam.shear_middle_string == "4L-T12@200"
    assert example_beam.shear_right_string == "4L-T12@100"

    assert example_beam.shear_left_area == approx(46234, 2)
    assert example_beam.shear_middle_area == approx(2261, 2)
    assert example_beam.shear_right_area == approx(46234, 2)
