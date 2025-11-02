from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class QueenState:
    row: int
    cols: set[int]
    diag_down: set[int]  # r - c
    diag_up: set[int]    # r + c
    pos: List[int]       # pos[r] = c of queen in row r


def solve_n_queens(n: int) -> list[list[str]]:
    """
    Return all distinct N-Queens boards of size `n`.

    Template recap (easy to remember):
      backtrack(state):
        if goal(state): record(state); return
        for choice in ordered_choices(state):
          if violates_constraint(state, choice): continue  # prune
          apply(state, choice)
          backtrack(state)
          undo(state, choice)

    Constraints encoded as sets:
    - `cols`: used columns
    - `diag_down`: r - c (top-left to bottom-right)
    - `diag_up`: r + c (bottom-left to top-right)

    Examples
    --------
    >>> solve_n_queens(1)
    [['Q']]
    >>> solve_n_queens(4)
    [['.Q..', '...Q', 'Q...', '..Q.'], ['..Q.', 'Q...', '...Q', '.Q..']]

    See also
    --------
    - `src.backtracking.n_queens_ii.total_n_queens` (count only)
    - `src.backtracking.n_queens_ii.count_n_queens` (alias)
    """

    if n <= 0:
        return []

    result: list[list[str]] = []
    state = QueenState(row=0, cols=set(), diag_down=set(), diag_up=set(), pos=[-1] * n)

    def goal(s: QueenState) -> bool:
        return s.row == n

    def record(s: QueenState) -> None:
        board: list[str] = []
        for r in range(n):
            c = s.pos[r]
            row_str = '.' * c + 'Q' + '.' * (n - c - 1)
            board.append(row_str)
        result.append(board)

    def ordered_choices(_: QueenState) -> range:
        return range(n)

    def violates_constraint(s: QueenState, col: int) -> bool:
        r = s.row
        return (
            col in s.cols or
            (r - col) in s.diag_down or
            (r + col) in s.diag_up
        )

    def apply(s: QueenState, col: int) -> None:
        r = s.row
        s.pos[r] = col
        s.cols.add(col)
        s.diag_down.add(r - col)
        s.diag_up.add(r + col)
        s.row += 1

    def undo(s: QueenState, col: int) -> None:
        s.row -= 1
        r = s.row
        s.pos[r] = -1
        s.cols.remove(col)
        s.diag_down.remove(r - col)
        s.diag_up.remove(r + col)

    def backtrack(s: QueenState) -> None:
        if goal(s):
            record(s)
            return
        for col in ordered_choices(s):
            if violates_constraint(s, col):
                continue
            apply(s, col)
            backtrack(s)
            undo(s, col)

    backtrack(state)
    return result


__all__ = ["solve_n_queens"]
