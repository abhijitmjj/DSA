from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence


@dataclass
class Subsets2State:
    start: int
    current: List[int]
    start_stack: List[int]


def subsets_unique(nums: Sequence[int]) -> list[list[int]]:
    """
    Subsets II: return all distinct subsets when `nums` may contain duplicates.

    Idea to remember:
    - Sort first. At each depth, skip equal values you've already tried
      at that depth: `if i > start and cand[i] == cand[i-1]: continue`.
    - Build combinations in increasing index order so order inside a subset
      doesn't matter.

    This uses the same backtracking skeleton with apply/undo on a shared state.

    Examples:
      >>> subsets_unique([1, 2, 2])
      [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
    """

    cand = sorted(nums)
    result: list[list[int]] = []
    state = Subsets2State(start=0, current=[], start_stack=[])

    def record(s: Subsets2State) -> None:
        result.append(s.current.copy())

    def ordered_choices(s: Subsets2State) -> range:
        return range(s.start, len(cand))

    def violates_constraint(s: Subsets2State, idx: int) -> bool:
        # Skip duplicates at the same recursion depth.
        return idx > s.start and cand[idx] == cand[idx - 1]

    def apply(s: Subsets2State, idx: int) -> None:
        s.current.append(cand[idx])
        s.start_stack.append(s.start)
        s.start = idx + 1

    def undo(s: Subsets2State, idx: int) -> None:
        s.current.pop()
        s.start = s.start_stack.pop()

    def backtrack(s: Subsets2State) -> None:
        # For subsets, every node is a valid subset.
        record(s)
        for idx in ordered_choices(s):
            if violates_constraint(s, idx):
                continue
            apply(s, idx)
            backtrack(s)
            undo(s, idx)

    backtrack(state)
    return result


__all__ = ["subsets_unique"]

