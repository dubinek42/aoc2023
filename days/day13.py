from typing import Any

from numpy.typing import NDArray

from .utils import get_2d_map


def part1(day_input: str) -> int:
    return _run(day_input)


def part2(day_input: str) -> int:
    return _run(day_input, 1)


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
        100 * _find_mirror(get_2d_map(p), smudge)
        + _find_mirror(get_2d_map(p).T, smudge)
        for p in day_input.split("\n\n")
    )
