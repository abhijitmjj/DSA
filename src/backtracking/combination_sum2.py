from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence


@dataclass
class Comb2State:
    start: int
    current: List[int]
    remaining: int
    start_stack: List[int]


def combination_sum2(nums: Sequence[int], target: int) -> list[list[int]]:
    """
    Combination Sum II — each number may be used at most once.

    - `nums` may contain duplicates; output must have unique combinations.
    - Order inside a combination doesn't matter; we build using increasing indices.
    - Classic tricks: sort, skip equal values at the same depth, and advance start.

    Template reminder:
      backtrack(state):
        if goal(state): record(state); return
        for choice in ordered_choices(state):
          if violates_constraint(state, choice): continue  # prune
          apply(state, choice)
          backtrack(state)
          undo(state, choice)

    Examples:
      >>> combination_sum2([10,1,2,7,6,1,5], 8)
      [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
      >>> combination_sum2([2,5,2,1,2], 5)
      [[1, 2, 2], [5]]
    """

    if target < 0:
        return []

    cand = sorted(nums)
    result: list[list[int]] = []
    state = Comb2State(start=0, current=[], remaining=target, start_stack=[])

    def goal(s: Comb2State) -> bool:
        return s.remaining == 0

    def record(s: Comb2State) -> None:
        result.append(s.current.copy())

    def ordered_choices(s: Comb2State) -> range:
        return range(s.start, len(cand))

    def violates_constraint(s: Comb2State, idx: int) -> bool:
        if cand[idx] > s.remaining:
            return True
        # Skip equal values at the same depth to prevent duplicate combinations.
        if idx > s.start and cand[idx] == cand[idx - 1]:
            return True
        return False

    def apply(s: Comb2State, idx: int) -> None:
        s.current.append(cand[idx])
        s.remaining -= cand[idx]
        # Use each number at most once → next choices start after idx.
        s.start_stack.append(s.start)
        s.start = idx + 1

    def undo(s: Comb2State, idx: int) -> None:
        s.remaining += cand[idx]
        s.current.pop()
        s.start = s.start_stack.pop()

    def backtrack(s: Comb2State) -> None:
        if goal(s):
            record(s)
            return

        for idx in ordered_choices(s):
            if violates_constraint(s, idx):
                # Because candidates are sorted, if value > remaining we can break early.
                if cand[idx] > s.remaining:
                    break
                continue
            apply(s, idx)
            backtrack(s)
            undo(s, idx)

    backtrack(state)
    return result


__all__ = ["combination_sum2"]
