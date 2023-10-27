import pytest
from beamscheduler.beam_calculator_class import Beam


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
        width=300,
        depth=500,
        pos_flex_combo="False",
        neg_flex_combo="False",
        req_top_flex_reinf=[441, 441, 441],
        req_bot_flex_reinf=[441, 441, 441],
        req_flex_torsion_reinf=[0, 0, 0],
        shear_combo="False",
        torsion_combo="False",
        req_shear_reinf=[1595.98, 1596.18, 800.44],
        req_torsion_reinf=[0, 0, 0],
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
    assert example_beam.flex_rebar_count == 2


def test_get_flex_top_req(example_beam: Beam):
    """This test checks if the correct flexural reinforcement values are obtained.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.flex_torsion_splitting()
    assert example_beam.req_top_flex_reinf == [
        441,
        441,
        441,
    ] and example_beam.req_flex_torsion_reinf == [0, 0, 0]


def test_get_flex_bot_req(example_beam: Beam):
    """This test checks if the correct flexural reinforcement values are obtained.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.flex_torsion_splitting()
    assert example_beam.req_bot_flex_reinf == [
        441,
        441,
        441,
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
    assert example_beam.flex_top_left_rebar_string == "3T16"
    assert example_beam.flex_top_middle_rebar_string == "3T16"
    assert example_beam.flex_top_middle_rebar_string == "3T16"


def test_bot_flex_rebar_string(example_beam: Beam):
    """This test checks that the bottom flexural rebar matches what would be expected for
    the required area of steel.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_long_count()
    example_beam.flex_torsion_splitting()
    example_beam.get_bot_flex_rebar_string()
    assert example_beam.flex_bot_left_rebar_string == "3T16"
    assert example_beam.flex_bot_middle_rebar_string == "3T16"
    assert example_beam.flex_bot_middle_rebar_string == "3T16"


def test_top_flex_rebar_area(example_beam: Beam):
    """This test checks that the top flexural rebar matches what would be expected for
    the required area of steel.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_long_count()
    example_beam.flex_torsion_splitting()
    example_beam.get_top_flex_rebar_area()
    assert example_beam.flex_top_left_rebar_area > 441 or example_beam.flex_top_left_rebar_area == 603  # type: ignore
    assert example_beam.flex_top_middle_rebar_area > 441 or example_beam.flex_top_left_rebar_area == 603  # type: ignore
    assert example_beam.flex_top_middle_rebar_area > 441 or example_beam.flex_top_left_rebar_area == 603  # type: ignore


def test_bot_flex_rebar_area(example_beam: Beam):
    """This test checks that the bottom flexural rebar matches what would be expected for
    the required area of steel.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_long_count()
    example_beam.flex_torsion_splitting()
    example_beam.get_bot_flex_rebar_area()
    assert example_beam.flex_bot_left_rebar_area > 441 or example_beam.flex_bot_left_rebar_area == 603  # type: ignore
    assert example_beam.flex_bot_middle_rebar_area > 441 or example_beam.flex_bot_left_rebar_area == 603  # type: ignore
    assert example_beam.flex_bot_middle_rebar_area > 441 or example_beam.flex_bot_left_rebar_area == 603  # type: ignore


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
    assert example_beam.left_residual_rebar == (example_beam.flex_bot_left_rebar_area - 441) * 2  # type: ignore
    assert example_beam.middle_residual_rebar == (example_beam.flex_bot_middle_rebar_area - 441) * 2  # type: ignore
    assert example_beam.right_residual_rebar == (example_beam.flex_bot_right_rebar_area - 441) * 2  # type: ignore


def test_total_shear_req(example_beam: Beam):
    """This test checks that the total shear requirement is correctly calculated.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_total_shear_req()
    assert example_beam.req_total_left_shear_reinf == 1595.98
    assert example_beam.req_total_middle_shear_reinf == 1596.18
    assert example_beam.req_total_right_shear_reinf == 800.44


def test_shear_legs(example_beam: Beam):
    """This test checks that the required shear legs is correctly obtained.
    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_shear_legs()
    assert example_beam.req_shear_legs == 2


def test_get_shear_string(example_beam: Beam):
    """This test checks that the obtained shear string is what is expected prior to checking the
    minimum spacing and filtering.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_total_shear_req()
    example_beam.get_shear_legs()
    example_beam.get_shear_string()
    assert example_beam.shear_left_string == "2L-T12@100"
    assert example_beam.shear_middle_string == "2L-T12@100"
    assert example_beam.shear_right_string == "2L-T12@250"


def test_shear_area(example_beam: Beam):
    """This test checks that the obtained shear area is what is expected prior to checking
    the minimum spacing and filtering.

    Args:
        example_beam (Beam): Refer to example beam function
    """
    example_beam.get_total_shear_req()
    example_beam.get_shear_legs()
    example_beam.get_shear_area()
    assert example_beam.shear_left_area == 2260
    assert example_beam.shear_middle_area == 2260
    assert example_beam.shear_right_area == 904
