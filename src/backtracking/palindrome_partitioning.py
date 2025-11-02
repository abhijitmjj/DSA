from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class PartState:
    start: int
    parts: List[str]


def palindrome_partition(s: str) -> list[list[str]]:
    """
    Return all ways to split `s` so every substring is a palindrome.

    Template recap (easy to memorize):
      backtrack(state):
        if goal(state): record(state); return
        for choice in ordered_choices(state):
          if violates_constraint(state, choice): continue  # prune
          apply(state, choice)
          backtrack(state)
          undo(state, choice)

    Approach
    --------
    - Precompute a boolean table `pal[i][j]` telling if `s[i:j+1]` is a
      palindrome in O(n^2) time.
    - From each `start`, try all `end >= start` with `pal[start][end]` true.
    - Apply/undo push/pop the chosen substring, moving `start` forward.

    Examples
    --------
    >>> palindrome_partition("aab")
    [['a', 'a', 'b'], ['aa', 'b']]
    >>> palindrome_partition("a")
    [['a']]
    """

    n = len(s)
    if n == 0:
        return [[]]

    # Precompute palindromes: pal[i][j] is True if s[i:j+1] is a palindrome.
    pal = [[False] * n for _ in range(n)]
    for i in range(n):
        pal[i][i] = True
    for i in range(n - 1):
        pal[i][i + 1] = s[i] == s[i + 1]
    for length in range(3, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            pal[i][j] = s[i] == s[j] and pal[i + 1][j - 1]

    result: list[list[str]] = []
    state = PartState(start=0, parts=[])

    def goal(st: PartState) -> bool:
        return st.start == n

    def record(st: PartState) -> None:
        result.append(st.parts.copy())

    def ordered_choices(st: PartState) -> range:
        return range(st.start, n)

    def violates_constraint(st: PartState, end: int) -> bool:
        return not pal[st.start][end]

    def apply(st: PartState, end: int) -> None:
        st.parts.append(s[st.start : end + 1])
        st.start = end + 1

    def undo(st: PartState, end: int) -> None:
        # restore start to previous substring's beginning
        st.start = end + 1 - len(st.parts[-1])  # compute previous start
        st.parts.pop()

    def backtrack(st: PartState) -> None:
        if goal(st):
            record(st)
            return
        for end in ordered_choices(st):
            if violates_constraint(st, end):
                continue
            prev_start = st.start
            apply(st, end)
            backtrack(st)
            # undo requires the original previous start
            st.start = prev_start
            undo(st, end)

    backtrack(state)
    return result


# Common LeetCode name
def partition(s: str) -> list[list[str]]:
    return palindrome_partition(s)


__all__ = ["palindrome_partition", "partition"]

