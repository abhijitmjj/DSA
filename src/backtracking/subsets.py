from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Hashable, Sequence, TypeVar

T = TypeVar("T", bound=Hashable)


@dataclass
class SubsetState(Generic[T]):
    cursor: int
    current: list[T]


def subsets(items: Sequence[T]) -> list[list[T]]:
    """
    Return every distinct subset of ``items`` while preserving the input order.

    Duplicate values in ``items`` yield only one copy of each subset.
    """
    result: list[list[T]] = []
    seen: set[tuple[T, ...]] = set()
    state = SubsetState(cursor=0, current=[])

    def goal(current_state: SubsetState[T]) -> bool:
        return current_state.cursor == len(items)

    def record(current_state: SubsetState[T]) -> None:
        snapshot = tuple(current_state.current)
        if snapshot in seen:
            return
        seen.add(snapshot)
        result.append(list(snapshot))

    def ordered_choices(current_state: SubsetState[T]) -> tuple[bool, ...]:
        if current_state.cursor >= len(items):
            return ()
        return (False, True)

    def violates_constraint(_: SubsetState[T], __: bool) -> bool:
        return False

    def apply(current_state: SubsetState[T], choice: bool) -> None:
        item = items[current_state.cursor]
        if choice:
            current_state.current.append(item)
        current_state.cursor += 1

    def undo(current_state: SubsetState[T], choice: bool) -> None:
        current_state.cursor -= 1
        if choice:
            current_state.current.pop()

    def backtrack(current_state: SubsetState[T]) -> None:
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


__all__ = ["subsets"]

if __name__ == "__main__":
    example = ["a", "b", "c"]
    print(subsets(example))
    example = [1, 2, 2]
    print(subsets(example))
