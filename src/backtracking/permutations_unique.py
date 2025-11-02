from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Hashable, Sequence, TypeVar

T = TypeVar("T", bound=Hashable)


@dataclass
class PermutationState(Generic[T]):
    current: list[T]
    used: list[bool]
    depth_seen: list[set[T]]


def permutations_unique(items: Sequence[T]) -> list[list[T]]:
    """
    Return all unique permutations of ``items`` (may contain duplicates).

    Template recap (easy to remember):
      backtrack(state):
        if goal(state): record(state); return
        for choice in ordered_choices(state):
          if violates_constraint(state, choice): continue  # prune
          apply(state, choice)
          backtrack(state)
          undo(state, choice)

    How duplicates are handled:
    - `used[i]` enforces each index is picked at most once per permutation.
    - `level_seen` (per depth) ensures we try each value only once at that
      depth, skipping symmetric branches when equal values exist.

    Examples
    --------
    >>> permutations_unique([1, 1, 2])
    [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
    >>> permutations_unique([1, 2, 3])
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    """

    result: list[list[T]] = []
    state = PermutationState(
        current=[],
        used=[False] * len(items),
        depth_seen=[set() for _ in range(len(items) + 1)],
    )

    def goal(current_state: PermutationState[T]) -> bool:
        return len(current_state.current) == len(items)

    def record(current_state: PermutationState[T]) -> None:
        result.append(current_state.current.copy())

    def ordered_choices(_: PermutationState[T]) -> range:
        return range(len(items))

    def violates_constraint(current_state: PermutationState[T], choice: int) -> bool:
        return current_state.used[choice]

    def apply(current_state: PermutationState[T], choice: int) -> None:
        current_state.used[choice] = True
        current_state.current.append(items[choice])

    def undo(current_state: PermutationState[T], choice: int) -> None:
        current_state.current.pop()
        current_state.used[choice] = False

    def backtrack(current_state: PermutationState[T]) -> None:
        if goal(current_state):
            record(current_state)
            return

        depth = len(current_state.current)
        level_seen = current_state.depth_seen[depth]
        level_seen.clear()

        for choice in ordered_choices(current_state):
            if violates_constraint(current_state, choice):
                continue
            value = items[choice]
            if value in level_seen:
                continue
            level_seen.add(value)
            apply(current_state, choice)
            backtrack(current_state)
            undo(current_state, choice)

    backtrack(state)
    return result


__all__ = ["permutations_unique"]


# from typing import Sequence, TypeVar, Hashable

# T = TypeVar("T", bound=Hashable)

# def permutations_unique_sorted(items: Sequence[T]) -> list[list[T]]:
#     a = sorted(items)                     # ensures duplicates are adjacent
#     n = len(a)
#     used = [False] * n
#     out: list[list[T]] = []
#     path: list[T] = []

#     def dfs():
#         if len(path) == n:           # Goal
#             out.append(path.copy())  # Record
#             return
#         for i in range(n):
#             if used[i]:              # Constraint violation
#                 continue
#             # skip duplicates: only use the first unused copy at this depth
#             if i > 0 and a[i] == a[i - 1] and not used[i - 1]:  
#                 continue
#             used[i] = True
#             path.append(a[i])        # Apply
#             dfs()                    # Recurse
#             path.pop()               # Undo
#             used[i] = False          # Undo

#     dfs()
#     return out
