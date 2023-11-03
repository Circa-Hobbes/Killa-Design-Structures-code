import pytest
from beamscheduler.beam_calculator_class import Beam
from pytest import approx


@pytest.mark.parametrize(
    "width, expected",
    [
        ("B600X600-C45/56", 600),
        ("B6X600-C45/56", 6),
        ("B60X600-C45/56", 60),
        ("B6000X600-C45/56", 6000),
    ],
)
def test_get_width(width: str, expected: int) -> int:
    """This function tests the get width method from the Beam class.

    Args:
        width (str): the width string obtained from ETABS.
        expected (int): the correct width in int dataform.

    Returns:
        int: the correct width in int dataform.
    """
    assert Beam.get_width(width) == expected


@pytest.mark.parametrize(
    "depth, expected",
    [
        ("B600X600-C45/56", 600),
        ("B600X6-C45/56", 6),
        ("B600X60-C45/56", 60),
        ("B600X6000-C45/56", 6000),
    ],
)
def test_get_depth(depth: str, expected: int) -> int:
    """This function tests the get width method from the Beam class.

    Args:
        depth (str): the depth string obtained from ETABS.
        expected (int): the correct depth in int dataform.

    Returns:
        int: the correct depth in int dataform.
    """
    assert Beam.get_depth(depth) == expected


@pytest.mark.parametrize(
    "diameter, expected",
    [
        (12, approx(113.1, 0.001)),
        (16, approx(201.06, 0.001)),
        (20, approx(314.16, 0.001)),
        (25, approx(490.87, 0.001)),
        (32, approx(804.25, 0.001)),
    ],
)
def test_provided_reinforcement(diameter: int, expected: int) -> float:
    """This function tests the provided reinforcement method from the Beam class.

    Args:
        diameter (int): The diameter of rebar
        expected (int): The area of steel (mm^2)

    Returns:
        float: The area of steel (mm^2)
    """
    assert Beam.provided_reinforcement(diameter) == expected
