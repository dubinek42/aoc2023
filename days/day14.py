from collections import Counter
from typing import Any

import numpy as np
from numpy.typing import NDArray

from .utils import get_2d_map


def part1(day_input: str) -> int:
    rock_map = get_2d_map(day_input)
    rock_map = _move_north(rock_map)
    total_load = _total_load(rock_map)
    return total_load


def part2(day_input: str) -> int:
    rock_map = get_2d_map(day_input)
    loads = []
    cycles_done = 0
    while True:
        cycles_done += 1
        rock_map = _move_cycle(rock_map)
        loads.append(_total_load(rock_map))
        if (repeat := _find_repeat(loads)) > 1:
            break
    repeat_start = len(loads) - 2 * repeat
    cycles_end = repeat_start + (1000000000 - repeat_start) % repeat
    return loads[cycles_end - 1]


def _total_load(rock_map: NDArray[Any]) -> int:
    return sum((i + 1) * Counter(line)["O"] for i, line in enumerate(rock_map[::-1]))


def _move_north(rock_map: NDArray[Any]) -> NDArray[Any]:
    return _move(rock_map.T).T


def _move_west(rock_map: NDArray[Any]) -> NDArray[Any]:
    return _move(rock_map)


def _move_east(rock_map: NDArray[Any]) -> NDArray[Any]:
    return np.fliplr(_move(np.fliplr(rock_map)))


def _move_south(rock_map: NDArray[Any]) -> NDArray[Any]:
    return np.flipud(_move(np.flipud(rock_map).T).T)


def _move(rock_map: NDArray[Any]) -> NDArray[Any]:
    new_map = []
    for row in rock_map:
        new_row = []
        for i, c in enumerate(row):
            if c == "O":
                new_row.append("O")
                continue
            if c == "#":
                new_row += ["."] * (i - len(new_row))
                new_row.append("#")
        new_row += ["."] * (len(row) - len(new_row))
        new_map.append(new_row)
    return np.array(new_map)


def _move_cycle(rock_map: NDArray[Any]) -> NDArray[Any]:
    rock_map = _move_north(rock_map)
    rock_map = _move_west(rock_map)
    rock_map = _move_south(rock_map)
    return _move_east(rock_map)


def _find_repeat(a: list[int]) -> int:
    """Find index from the end of list, where patterns start repeating."""
    for i in range(1, len(a) // 2):
        if a[::-1][0:i] == a[::-1][i : i * 2]:
            return i
    return 0
