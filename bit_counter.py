#!/usr/bin/env python3
"""
bit_counter.py: count the number of set bits (1s) in the binary representation of a non-negative integer.
Usage:
    python bit_counter.py <number>
"""

from __future__ import annotations
import sys
from typing import NoReturn


def count_set_bits(n: int) -> int:
    """
    Count the number of bits set to 1 in the binary representation of a non-negative integer n.

    Args:
        n: A non-negative integer.

    Returns:
        An integer count of bits set to 1.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError(f"Negative value {n} is not allowed.")
    count: int = 0
    while n:
        # Increment count if the least significant bit is 1
        count += n & 1
        # Shift right by 1 to process the next bit
        n >>= 1
    return count


def main() -> NoReturn:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    try:
        num = int(sys.argv[1])
    except ValueError:
        print(f"Error: '{sys.argv[1]}' is not a valid integer.", file=sys.stderr)
        sys.exit(1)
    try:
        result = count_set_bits(num)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    print(result)
    sys.exit(0)


if __name__ == "__main__":
    main()
