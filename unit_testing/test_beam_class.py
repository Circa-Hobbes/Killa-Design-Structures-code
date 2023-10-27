import sys
import pytest

sys.path.append(
    r"C:\Users\adnan.a\OneDrive - Killa Design\Documents\GitHub\Killa-Design-Structures-code\V2_kld beam reinf code"
)

from beam_calculator_class import Beam


@pytest.fixture
def example_beam() -> object:
    """This example beam is utilised for testing purposes.
    Please define the attributes of the example beam in the following instance.
    Returns:
        object: example beam to utilise in tests.
    """
    example_beam = Beam(
        id=None,
        width=400,
        depth=900,
        pos_flex_combo="False",
        neg_flex_combo="False",
        req_top_flex_reinf=[1000, 1000, 1000],
        req_bot_flex_reinf=[1000, 1000, 1000],
        req_flex_torsion_reinf=[0, 0, 0],
        shear_combo="False",
        torsion_combo="False",
        req_shear_reinf=[0, 0, 0],
        req_torsion_reinf=[0, 0, 0],
    )
    return example_beam


def test_eff_depth(example_beam: Beam):
    example_beam.get_eff_depth()
    assert example_beam.eff_depth == 0.8 * example_beam.depth
