from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence


@dataclass
class KPartState:
    idx: int
    buckets: List[int]


def can_partition_k_subsets(nums: Sequence[int], k: int) -> bool:
    """
    Return True if `nums` can be split into `k` non-empty subsets
    with equal sum; otherwise False.

    Pattern (same interview-friendly backtracking template):
      backtrack(state):
        if goal(state): return True
        for choice in ordered_choices(state):
          if violates_constraint(state, choice): continue  # prune
          apply(state, choice)
          if backtrack(state): return True
          undo(state, choice)

    Strategy
    --------
    - Target per-bucket sum is `sum(nums) // k` (early return if not divisible).
    - Sort descending for stronger pruning.
    - Place the current element into one of the `k` buckets (subset sums).
    - Skip symmetric bucket states by remembering lengths tried at this depth
      and breaking after a failed attempt on an empty bucket.

    Examples
    --------
    >>> can_partition_k_subsets([2,4,1,3,5], 3)
    True
    >>> can_partition_k_subsets([1,2,3,4], 3)
    False
    """

    n = len(nums)
    if k <= 0 or k > n:
        return False

    total = sum(nums)
    if total % k != 0:
        return False
    target = total // k

    arr = sorted(nums, reverse=True)
    if arr[0] > target:
        return False

    state = KPartState(idx=0, buckets=[0] * k)

    def goal(s: KPartState) -> bool:
        return s.idx == n

    def ordered_choices(_: KPartState) -> range:
        return range(k)

    def violates_constraint(s: KPartState, choice: int) -> bool:
        return s.buckets[choice] + arr[s.idx] > target

    def apply(s: KPartState, choice: int) -> None:
        s.buckets[choice] += arr[s.idx]
        s.idx += 1

    def undo(s: KPartState, choice: int) -> None:
        s.idx -= 1
        s.buckets[choice] -= arr[s.idx]

    def backtrack(s: KPartState) -> bool:
        if goal(s):
            # All items placed; because of constraints, each bucket <= target.
            # Ensure all buckets reach the target sum.
            tgt = target
            return all(b == tgt for b in s.buckets)

        seen_lengths: set[int] = set()
        for choice in ordered_choices(s):
            length_before = s.buckets[choice]
            if length_before in seen_lengths:
                continue
            if violates_constraint(s, choice):
                continue
            seen_lengths.add(length_before)
            apply(s, choice)
            if backtrack(s):
                return True
            undo(s, choice)
            # If we tried putting current number into an empty bucket and failed,
            # no need to try other empty buckets (they are symmetric).
            if length_before == 0:
                break
        return False

    return backtrack(state)


__all__ = ["can_partition_k_subsets"]

