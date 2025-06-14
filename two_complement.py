#!/usr/bin/env python3
"""
two_complement.py: compute the two's complement representation of an integer.
Usage:
    python two_complement.py <number> <bits>
"""

from __future__ import annotations
import sys
from typing import NoReturn


def two_complement(n: int, bits: int) -> str:
    """
    Compute the two's complement binary representation of integer n in given bit width.

    Args:
        n: Integer to represent (can be negative or non-negative).
        bits: Bit width (must be a positive integer).

    Returns:
        A binary string of length `bits` representing the two's complement of n.

    Raises:
        ValueError: If bits <= 0 or n is out of the representable range.
    """
    if bits <= 0:
        raise ValueError(f"Bit width must be positive, got {bits}.")
    min_val = -(1 << (bits - 1))
    max_val = (1 << (bits - 1)) - 1
    if n < min_val or n > max_val:
        raise ValueError(
            f"Value {n} out of range [{min_val}, {max_val}] for {bits}-bit two's complement."
        )
    mask = (1 << bits) - 1
    return format(n & mask, f"0{bits}b")


def negate(n: int, bits: int) -> str:
    """
    Compute the two's complement representation of the negation of n using bitwise operations.

    Args:
        n: Integer to negate (must be within representable signed range).
        bits: Bit width (must be a positive integer).

    Returns:
        A binary string of length `bits` representing the two's complement of -n.

    Raises:
        ValueError: If bits <= 0 or n is out of representable signed range.
    """
    if bits <= 0:
        raise ValueError(f"Bit width must be positive, got {bits}.")
    min_val = -(1 << (bits - 1))
    max_val = (1 << (bits - 1)) - 1
    if n < min_val or n > max_val:
        raise ValueError(
            f"Value {n} out of range [{min_val}, {max_val}] for {bits}-bit two's complement."
        )
    mask = (1 << bits) - 1
    # Mask to obtain n's two's-complement representation
    n_masked = n & mask
    # One's complement (bitwise inversion)
    inverted = (~n_masked) & mask
    # Add one to get two's complement negation
    negated = (inverted + 1) & mask
    return format(negated, f"0{bits}b")


def main() -> NoReturn:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    try:
        num = int(sys.argv[1])
        bits = int(sys.argv[2])
    except ValueError:
        print(
            f"Error: invalid integer input '{sys.argv[1]}' or bits '{sys.argv[2]}'.",
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        result = two_complement(num, bits)
        negated_result = negate(num, bits)
        print(f"Two's complement: {result}, Negation: {negated_result}")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
