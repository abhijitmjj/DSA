from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Sequence


@dataclass
class WBState:
    index: int


def word_break(s: str, word_dict: Sequence[str]) -> list[str]:
    """
    Return all sentences by inserting spaces in `s` so every piece is in `word_dict`.

    Template recap (conceptual):
      backtrack(state):
        if goal(state): record(state); return
        for choice in ordered_choices(state):
          if violates_constraint(state, choice): continue  # prune
          apply(state, choice)
          backtrack(state)
          undo(state, choice)

    Implementation notes:
    - We memoize by start index to avoid recomputing suffix solutions.
    - Iterate next cut positions up to `max_word_len` for efficient pruning.

    Examples
    --------
    >>> word_break("neetcode", ["neet", "code"])
    ['neet code']
    >>> word_break("racecariscar", ["racecar", "race", "car", "is"])
    ['racecar is car', 'race car is car']
    >>> word_break("catsincars", ["cats", "cat", "sin", "in", "car"])
    []
    """

    n = len(s)
    if n == 0:
        return []

    words = set(word_dict)
    if not words:
        return []

    max_len = max(len(w) for w in words)

    @lru_cache(maxsize=None)
    def dfs(i: int) -> list[str]:
        if i == n:
            return [""]
        out: list[str] = []
        end_limit = min(n, i + max_len)
        for j in range(i + 1, end_limit + 1):
            piece = s[i:j]
            if piece not in words:
                continue
            for tail in dfs(j):
                out.append(piece if tail == "" else f"{piece} {tail}")
        return out

    return dfs(0)


__all__ = ["word_break"]


# Template-style backtracking variant (explicit apply/undo state)
from typing import List
from dataclasses import dataclass


@dataclass
class WBTemplateState:
    index: int
    parts: List[str]
    index_stack: List[int]


def word_break_template(s: str, word_dict: Sequence[str]) -> list[str]:
    """
    Word Break II solved with the explicit backtracking template.

      backtrack(state):
        if goal(state): record(state); return
        for choice in ordered_choices(state):
          if violates_constraint(state, choice): continue  # prune
          apply(state, choice)
          backtrack(state)
          undo(state, choice)

    Notes
    -----
    - Uses a small `bad` set to prune indices that cannot reach the end.
    - Limits candidate cuts to `max_word_len` for efficiency.
    - Builds sentences by joining `parts` on record.
    """

    n = len(s)
    if n == 0:
        return []

    words = set(word_dict)
    if not words:
        return []

    max_len = max(len(w) for w in words)
    result: list[str] = []
    bad: set[int] = set()
    state = WBTemplateState(index=0, parts=[], index_stack=[])

    def goal(st: WBTemplateState) -> bool:
        return st.index == n

    def record(st: WBTemplateState) -> None:
        result.append(" ".join(st.parts))

    def ordered_choices(st: WBTemplateState) -> range:
        end_limit = min(n, st.index + max_len)
        return range(st.index + 1, end_limit + 1)

    def violates_constraint(st: WBTemplateState, end: int) -> bool:
        return s[st.index:end] not in words

    def apply(st: WBTemplateState, end: int) -> None:
        st.parts.append(s[st.index:end])
        st.index_stack.append(st.index)
        st.index = end

    def undo(st: WBTemplateState, _: int) -> None:
        st.index = st.index_stack.pop()
        st.parts.pop()

    def backtrack(st: WBTemplateState) -> bool:
        if st.index in bad:
            return False
        if goal(st):
            record(st)
            return True
        found = False
        for end in ordered_choices(st):
            if violates_constraint(st, end):
                continue
            apply(st, end)
            if backtrack(st):
                found = True
            undo(st, end)
        if not found:
            bad.add(st.index)
        return found

    backtrack(state)
    return result


__all__.extend(["word_break_template"])
