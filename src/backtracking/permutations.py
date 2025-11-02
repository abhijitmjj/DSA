from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Sequence, TypeVar

T = TypeVar("T")


@dataclass
class PermutationState(Generic[T]):
    current: list[T]
    used: list[bool]


def permutations(items: Sequence[T]) -> list[list[T]]:
    """
    Generate every permutation of ``items`` in lexical order of positions.

    The routine stays close to the classic backtracking interview template:
    track which indices are already in the partial solution, extend with
    each remaining choice, and undo before the next branch.
    """

    result: list[list[T]] = []
    state = PermutationState(current=[], used=[False] * len(items))

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

        for choice in ordered_choices(current_state):
            if violates_constraint(current_state, choice):
                continue
            apply(current_state, choice)
            backtrack(current_state)
            undo(current_state, choice)

    backtrack(state)
    return result


__all__ = ["permutations"]
