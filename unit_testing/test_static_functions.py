import pytest
from beamscheduler.beam_calculator_class import Beam


@pytest.mark.parametrize("width, expected", [("B600X600-C45/56", 600)])
def test_get_width(width: str, expected: int) -> int:
    """This function tests the get width method from the Beam class.

    Args:
        width (str): the width string obtained from ETABS.
        expected (int): the correct width in int dataform.

    Returns:
        int: the correct width in int dataform.
    """
    assert Beam.get_width(width) == expected


@pytest.mark.parametrize("depth, expected", [("B600X600-C45/56", 600)])
def test_get_depth(depth: str, expected: int) -> int:
    """This function tests the get width method from the Beam class.

    Args:
        depth (str): the depth string obtained from ETABS.
        expected (int): the correct depth in int dataform.

    Returns:
        int: the correct depth in int dataform.
    """
    assert Beam.get_depth(depth) == expected
