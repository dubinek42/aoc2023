from typing import Any

import numpy as np
from numpy.typing import NDArray


def part1(day_input: str) -> int:
    return _run(day_input)


def part2(day_input: str) -> int:
    return _run(day_input, 1)


def _get_pattern_map(pattern: str) -> NDArray[Any]:
    return np.array([list(x) for x in pattern.splitlines()])


def _find_mirror(pattern: NDArray[Any], smudge: int) -> int:
    for i in range(1, len(pattern)):
        a = pattern[:i][::-1]
        b = pattern[i:]
        point = min(len(a), len(b))
        if (a[:point] != b[:point]).sum() == smudge:
            return i
    return 0


def _run(day_input: str, smudge: int = 0) -> int:
    return sum(
        100 * _find_mirror(_get_pattern_map(p), smudge)
        + _find_mirror(_get_pattern_map(p).T, smudge)
        for p in day_input.split("\n\n")
    )
