from itertools import combinations
from typing import Any

import numpy as np
from numpy.typing import NDArray


def part1(day_input: str) -> int:
    return count_galaxy_distances(_get_galaxy_map(day_input), expand_factor=2)


def part2(day_input: str) -> int:
    return count_galaxy_distances(_get_galaxy_map(day_input), expand_factor=1000000)


def count_galaxy_distances(galaxy_map: NDArray[Any], expand_factor: int) -> int:
    return sum(
        _distance(a, b)
        for a, b in list(combinations(_expand_galaxies(galaxy_map, expand_factor), 2))
    )


def _get_galaxy_map(day_input: str) -> NDArray[Any]:
    return np.array([list(x) for x in day_input.splitlines()])


def _get_empty_space(galaxy_map: NDArray[Any]) -> tuple[list[int], ...]:
    rows = [i for i, row in enumerate(galaxy_map) if np.all(row == ".")]
    cols = [i for i, col in enumerate(galaxy_map.T) if np.all(col == ".")]
    return rows, cols


def _get_galaxies(galaxy_map: NDArray[Any]) -> list[tuple[int, int]]:
    return list(map(tuple, np.argwhere(galaxy_map == "#")))


def _expand_galaxies(galaxy_map: NDArray[Any], constant: int) -> list[tuple[int, int]]:
    galaxies = _get_galaxies(galaxy_map)
    empty_rows, empty_cols = _get_empty_space(galaxy_map)
    new_galaxies = []
    for g in galaxies:
        x = len([n for n in empty_rows if g[0] > n])
        y = len([n for n in empty_cols if g[1] > n])
        new_galaxies.append((g[0] + x * constant - x, g[1] + y * constant - y))
    return new_galaxies


def _distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(b[0] - a[0]) + abs(b[1] - a[1])
