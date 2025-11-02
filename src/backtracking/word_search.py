from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence, Tuple


Coord = Tuple[int, int]


@dataclass
class WordState:
    r: int
    c: int
    i: int  # index into word for the character at (r, c)


def exist(board: Sequence[Sequence[str]], word: str) -> bool:
    """
    Return True if `word` exists in `board` via an adjacent (4-dir) path.

    - You may not reuse a cell within the same path.
    - Board cells are matched sequentially to characters in `word`.

    Template recap (backtracking):
      backtrack(state):
        if goal(state): return True
        for choice in ordered_choices(state):
          if violates_constraint(state, choice): continue  # prune
          apply(state, choice)
          if backtrack(new_state): return True
          undo(state, choice)

    Examples
    --------
    >>> board = [
    ...   ["A","B","C","D"],
    ...   ["S","A","A","T"],
    ...   ["A","C","A","E"],
    ... ]
    >>> exist(board, "CAT")
    True
    >>> exist(board, "BAT")
    False
    """

    if not word:
        return True

    rows = len(board)
    cols = len(board[0]) if rows else 0
    if rows == 0 or cols == 0:
        return False

    # Small letter-frequency sanity prune (optional but cheap):
    # If board lacks a required char multiplicity, early exit.
    from collections import Counter

    wc = Counter(word)
    bc = Counter(ch for row in board for ch in row)
    if any(bc[ch] < need for ch, need in wc.items()):
        return False

    DIRS: tuple[Coord, ...] = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def neighbors(r: int, c: int) -> Iterable[Coord]:
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                yield (nr, nc)

    visited: set[Coord] = set()

    def goal(s: WordState) -> bool:
        # At a goal state, we have placed the last character of `word`.
        return s.i == len(word) - 1 and board[s.r][s.c] == word[s.i]

    def ordered_choices(s: WordState) -> Iterable[Coord]:
        return neighbors(s.r, s.c)

    def violates_constraint(s: WordState, nxt: Coord) -> bool:
        # Must be unvisited and match the next character.
        if nxt in visited:
            return True
        nr, nc = nxt
        next_i = s.i + 1  # lookahead index
        return board[nr][nc] != word[next_i]

    def apply(s: WordState, nxt: Coord) -> WordState:
        visited.add(nxt)
        nr, nc = nxt
        return WordState(nr, nc, s.i + 1)

    def undo(_: WordState, nxt: Coord) -> None:
        visited.remove(nxt)

    def backtrack(state: WordState) -> bool:
        if goal(state):
            return True
        for nxt in ordered_choices(state):
            # Only consider if next board cell equals the next char and unused.
            if state.i + 1 >= len(word):
                continue
            if violates_constraint(state, nxt):
                continue
            new_state = apply(state, nxt)
            if backtrack(new_state):
                return True
            undo(state, nxt)
        return False

    # Try all starts that match the first character.
    first = word[0]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != first:
                continue
            start = WordState(r, c, 0)
            visited.clear()
            visited.add((r, c))
            if backtrack(start):
                return True
            visited.remove((r, c))
    return False


__all__ = ["exist"]
