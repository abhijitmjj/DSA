import os
import sys

# Ensure project root is on the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from two_complement import two_complement, negate


@pytest.mark.parametrize(
    "n,bits,expected",
    [
        (0, 1, "0"),
        (0, 8, "00000000"),
        (1, 8, "00000001"),
        (-1, 8, "11111111"),
        (127, 8, "01111111"),
        (-128, 8, "10000000"),
        (5, 4, "0101"),
        (-5, 4, "1011"),
        (-1, 4, "1111"),
        (7, 4, "0111"),
    ],
)
def test_two_complement_valid(n, bits, expected):
    """Test two_complement with valid inputs."""
    assert two_complement(n, bits) == expected


@pytest.mark.parametrize(
    "n,bits",
    [
        (128, 8),
        (-129, 8),
        (2, 1),  # 1-bit range is [-1, 0]
    ],
)
def test_two_complement_out_of_range(n, bits):
    """Inputs outside representable range should raise ValueError."""
    with pytest.raises(ValueError):
        two_complement(n, bits)


@pytest.mark.parametrize(
    "n,bits",
    [
        (1, 0),
        (1, -1),
    ],
)
def test_two_complement_invalid_width(n, bits):
    """Non-positive bit widths should raise ValueError."""
    with pytest.raises(ValueError):
        two_complement(n, bits)
    # no changes to input n


@pytest.mark.parametrize(
    "n,bits,expected",
    [
        (5, 8, "11111011"),  # -5 in 8 bits
        (-5, 8, "00000101"),  # -(-5)=5 in 8 bits
        (0, 4, "0000"),  # negating zero
    ],
)
def test_negate_valid(n, bits, expected):
    """Test negate with valid inputs."""
    assert negate(n, bits) == expected


@pytest.mark.parametrize(
    "n,bits",
    [
        (1, 1),  # 1 not representable in 1-bit two's complement
        (5, 3),  # 5 out of range for 3-bit signed
    ],
)
def test_negate_out_of_range(n, bits):
    """Inputs outside representable range should raise ValueError."""
    with pytest.raises(ValueError):
        negate(n, bits)


@pytest.mark.parametrize(
    "n,bits",
    [
        (1, 0),
        (1, -2),
    ],
)
def test_negate_invalid_width(n, bits):
    """Non-positive bit widths should raise ValueError."""
    with pytest.raises(ValueError):
        negate(n, bits)
