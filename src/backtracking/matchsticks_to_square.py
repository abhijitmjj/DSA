from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence


@dataclass
class SquareState:
    idx: int
    sides: List[int]  # four side sums


def makesquare(matchsticks: Sequence[int]) -> bool:
    """
    Return True if all matchsticks can form a square, else False.

    Recipe to remember (backtracking template):
      backtrack(state):
        if goal(state): return True
        for choice in ordered_choices(state):
          if violates_constraint(state, choice): continue  # prune
          apply(state, choice)
          if backtrack(state): return True
          undo(state, choice)

    Notes
    -----
    - Target side length is total_sum // 4; if total_sum % 4 != 0, fail early.
    - Sort sticks in descending order to tighten pruning.
    - At each depth, skip sides with the same current length to avoid symmetry.

    Examples
    --------
    >>> makesquare([1,3,4,2,2,4])
    True
    >>> makesquare([1,5,6,3])
    False
    """

    n = len(matchsticks)
    if n < 4:
        return False

    total = sum(matchsticks)
    if total % 4 != 0:
        return False
    side = total // 4

    sticks = sorted(matchsticks, reverse=True)
    if sticks[0] > side:
        return False

    state = SquareState(idx=0, sides=[0, 0, 0, 0])

    def goal(s: SquareState) -> bool:
        return s.idx == n

    def ordered_choices(_: SquareState) -> range:
        return range(4)

    def violates_constraint(s: SquareState, choice: int) -> bool:
        return s.sides[choice] + sticks[s.idx] > side

    def apply(s: SquareState, choice: int) -> None:
        s.sides[choice] += sticks[s.idx]
        s.idx += 1

    def undo(s: SquareState, choice: int) -> None:
        s.idx -= 1
        s.sides[choice] -= sticks[s.idx]

    def backtrack(s: SquareState) -> bool:
        if goal(s):
            # If all sticks are placed and no side exceeds target, it's valid
            # because of constraints; optional: ensure all equal to target.
            return s.sides[0] == s.sides[1] == s.sides[2] == s.sides[3] == side

        seen_lengths: set[int] = set()
        for choice in ordered_choices(s):
            length_before = s.sides[choice]
            if length_before in seen_lengths:
                continue
            if violates_constraint(s, choice):
                continue
            seen_lengths.add(length_before)
            apply(s, choice)
            if backtrack(s):
                return True
            undo(s, choice)
            # If we put the stick on an empty side and it failed, no need to
            # try other empty sides (they are symmetric).
            if length_before == 0:
                break
        return False

    return backtrack(state)


__all__ = ["makesquare"]

