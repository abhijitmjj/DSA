import os
import sys

# Ensure the project root is on the import path to locate bit_counter.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from bit_counter import count_set_bits
from hypothesis import given, strategies as st


@pytest.mark.parametrize(
    "n,expected",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (10, 2),  # 0b1010
        (255, 8),  # 0b11111111
        (256, 1),  # 0b100000000
        (257, 2),  # 0b100000001
        (2**16 - 1, 16),
        (2**20 + 2**19 + 1, 3),
    ],
)
def test_count_set_bits_simple(n, expected):
    """
    Test count_set_bits with a variety of fixed inputs.
    """
    assert count_set_bits(n) == expected


def test_count_set_bits_zero():
    """Edge case: zero has zero bits set."""
    assert count_set_bits(0) == 0


def test_count_set_bits_negative_raises():
    """Negative inputs should raise ValueError."""
    with pytest.raises(ValueError):
        count_set_bits(-1)


@given(st.integers(min_value=0, max_value=10**6))
def test_count_set_bits_against_bin(n):
    """
    Property-based test: compare against Python's bin() for non-negative integers.
    """
    # bin(n) returns a string like '0b1011'
    expected = bin(n).count("1")
    assert count_set_bits(n) == expected
