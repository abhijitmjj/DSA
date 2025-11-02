from __future__ import annotations

from dataclasses import dataclass


@dataclass
class QueensCountState:
    row: int
    cols: int
    diag_down: int  # \ diagonal mask (r - c shifted via bit moves between rows)
    diag_up: int    # / diagonal mask (r + c shifted via bit moves between rows)
    cols_stack: list[int]
    diag_down_stack: list[int]
    diag_up_stack: list[int]
    count: int


def total_n_queens(n: int) -> int:
    """
    Return the number of distinct N-Queens solutions for board size `n`.

    Uses the same backtracking template with bit masks for O(1) constraint
    checks and fast branching:

      backtrack(state):
        if goal(state): record(state); return
        for choice in ordered_choices(state):
          if violates_constraint(state, choice): continue  # implicit in mask
          apply(state, choice)
          backtrack(state)
          undo(state, choice)

    Masks
    -----
    - `cols`: columns already used
    - `diag_down`: \\ diagonals (top-left to bottom-right), shifted left when going deeper
    - `diag_up`:   / diagonals (bottom-left to top-right), shifted right when going deeper

    Examples
    --------
    >>> total_n_queens(1)
    1
    >>> total_n_queens(4)
    2
    """

    if n <= 0:
        return 0

    all_ones = (1 << n) - 1
    state = QueensCountState(
        row=0, cols=0, diag_down=0, diag_up=0,
        cols_stack=[], diag_down_stack=[], diag_up_stack=[], count=0,
    )

    def goal(s: QueensCountState) -> bool:
        return s.row == n

    def record(s: QueensCountState) -> None:
        s.count += 1

    def ordered_choices(s: QueensCountState) -> int:
        # Bitmask of available columns at this row.
        return all_ones & ~(s.cols | s.diag_down | s.diag_up)

    def apply(s: QueensCountState, p: int) -> None:
        s.cols_stack.append(s.cols)
        s.diag_down_stack.append(s.diag_down)
        s.diag_up_stack.append(s.diag_up)
        s.cols |= p
        s.diag_down = (s.diag_down | p) << 1
        s.diag_up = (s.diag_up | p) >> 1
        s.row += 1

    def undo(s: QueensCountState, _: int) -> None:
        s.row -= 1
        s.diag_up = s.diag_up_stack.pop()
        s.diag_down = s.diag_down_stack.pop()
        s.cols = s.cols_stack.pop()

    def backtrack(s: QueensCountState) -> None:
        if goal(s):
            record(s)
            return
        avail = ordered_choices(s)
        while avail:
            p = avail & -avail  # pick least significant available bit
            avail -= p
            apply(s, p)
            backtrack(s)
            undo(s, p)

    backtrack(state)
    return state.count


def count_n_queens(n: int) -> int:
    """Alias for `total_n_queens` (LeetCode-style name)."""
    return total_n_queens(n)


__all__ = ["total_n_queens", "count_n_queens"]
