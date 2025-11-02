from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence


@dataclass
class CombState:
    start: int
    current: List[int]
    remaining: int


def combination_sum(nums: Sequence[int], target: int) -> list[list[int]]:
    """
    Return all unique combinations of `nums` that sum to `target`.

    - Each number may be used unlimited times.
    - Combinations ignore order (we build in non-decreasing index order).
    - `nums` is assumed distinct; we sort a local copy for pruning.

    Interview pattern to remember:
      backtrack(state):
        if goal(state): record(state); return
        for choice in ordered_choices(state):
          if violates_constraint(state, choice): continue  # prune
          apply(state, choice)
          backtrack(state)
          undo(state, choice)

    Example:
      >>> combination_sum([2, 5, 6, 9], 9)
      [[2, 2, 5], [9]]
    """

    if target < 0:
        return []

    cand = sorted(nums)
    result: list[list[int]] = []
    state = CombState(start=0, current=[], remaining=target)

    def goal(s: CombState) -> bool:
        return s.remaining == 0

    def record(s: CombState) -> None:
        result.append(s.current.copy())

    def ordered_choices(s: CombState) -> range:
        return range(s.start, len(cand))

    def violates_constraint(s: CombState, idx: int) -> bool:
        # Prune when the next candidate overshoots the remaining sum.
        return cand[idx] > s.remaining

    def apply(s: CombState, idx: int) -> None:
        s.current.append(cand[idx])
        s.remaining -= cand[idx]
        # Allow unlimited reuse of the same number: keep start at idx.
        s.start = idx

    def undo(s: CombState, idx: int) -> None:
        s.remaining += cand[idx]
        s.current.pop()
        # After undo, next loop iteration will try the next index; no change needed.

    def backtrack(s: CombState) -> None:
        if goal(s):
            record(s)
            return

        for idx in ordered_choices(s):
            if violates_constraint(s, idx):
                break  # because cand is sorted, larger ones will also violate
            apply(s, idx)
            backtrack(s)
            undo(s, idx)

    backtrack(state)
    return result


__all__ = ["combination_sum"]

