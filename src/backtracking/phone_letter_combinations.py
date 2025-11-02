from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence


KEYPAD: dict[str, str] = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}


@dataclass
class PhoneState:
    index: int
    current: List[str]


def letter_combinations(digits: str) -> list[str]:
    """
    Return all possible letter combinations the digit string could represent.

    Uses the standard phone keypad mapping for digits 2–9 and the
    backtracking interview template.

      backtrack(state):
        if goal(state): record(state); return
        for choice in ordered_choices(state):
          if violates_constraint(state, choice): continue  # prune
          apply(state, choice)
          backtrack(state)
          undo(state, choice)

    Notes
    -----
    - Returns an empty list for an empty input string (LeetCode convention).
    - Output order follows the digit order and mapping order.

    Examples
    --------
    >>> letter_combinations("34")
    ['dg', 'dh', 'di', 'eg', 'eh', 'ei', 'fg', 'fh', 'fi']
    >>> letter_combinations("")
    []
    """

    if not digits:
        return []

    # Validate digits and build a list of letter groups for each position.
    groups: list[str] = []
    for ch in digits:
        letters = KEYPAD.get(ch)
        if not letters:
            # If any invalid digit (e.g., '1' or '0') appears, return empty.
            return []
        groups.append(letters)

    result: list[str] = []
    state = PhoneState(index=0, current=[])

    def goal(s: PhoneState) -> bool:
        return s.index == len(groups)

    def record(s: PhoneState) -> None:
        result.append("".join(s.current))

    def ordered_choices(s: PhoneState) -> Sequence[str]:
        return groups[s.index]

    def violates_constraint(_: PhoneState, __: str) -> bool:
        return False

    def apply(s: PhoneState, ch: str) -> None:
        s.current.append(ch)
        s.index += 1

    def undo(s: PhoneState, _: str) -> None:
        s.index -= 1
        s.current.pop()

    def backtrack(s: PhoneState) -> None:
        if goal(s):
            record(s)
            return
        for ch in ordered_choices(s):
            if violates_constraint(s, ch):
                continue
            apply(s, ch)
            backtrack(s)
            undo(s, ch)

    backtrack(state)
    return result


__all__ = ["letter_combinations"]

