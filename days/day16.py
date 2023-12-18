from collections import deque
from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from .utils import get_2d_map, in_bounds


@dataclass
class Beam:
    position: complex
    direction: complex


def part1(day_input: str) -> int:
    contraption = get_2d_map(day_input)
    return _total_heat(contraption, complex(0, 0), complex(0, 1))


def part2(day_input: str) -> int:
    contraption = get_2d_map(day_input)
    return max(
        _total_heat(contraption, start, direction)
        for start, direction in _possible_starts(contraption.shape)
    )


def _total_heat(
    contraption: NDArray[Any],
    start_position: complex,
    start_direction: complex,
) -> int:
    first_tile = contraption[_uncomplex(start_position)]
    q: deque[Beam] = deque()
    q.extend(_new_beams(first_tile, start_position, start_direction))
    energized = np.zeros(contraption.shape)
    energized[_uncomplex(start_position)] = 1
    visited = set()

    while q:
        current: Beam = q.popleft()
        new_position = current.position + current.direction
        energized[_uncomplex(current.position)] = 1

        visit = (_uncomplex(new_position)), (_uncomplex(current.direction))
        if (
            not in_bounds(_uncomplex(new_position), contraption.shape)  # type: ignore[arg-type]
            or visit in visited
        ):
            continue

        visited.add(visit)
        tile = contraption[_uncomplex(new_position)]
        q.extend(_new_beams(tile, new_position, current.direction))
    return np.count_nonzero(energized)


def _uncomplex(number: complex) -> tuple[int, int]:
    return int(number.real), int(number.imag)


def _possible_starts(shape: tuple[int, ...]) -> list[tuple[complex, complex]]:
    rows, cols = shape
    result = []

    # left and right edge
    for i in range(rows):
        result.append((complex(i, 0), complex(0, 1)))
        result.append((complex(i, rows - 1), complex(0, -1)))
    # top and bottom edge
    for i in range(cols):
        result.append((complex(0, i), complex(1, 0)))
        result.append((complex(cols - 1, i), complex(-1, 0)))
    return result


def _new_beams(tile: str, position: complex, direction: complex) -> list[Beam]:
    def turn_left(d: complex) -> complex:
        return d * 1j

    def turn_right(d: complex) -> complex:
        return d * -1j

    # fmt: off
    beam_generators = {
        ".": lambda: [Beam(position, direction)],

        "|": lambda: [
                Beam(position, turn_left(direction)),
                Beam(position, turn_right(direction)),
            ]
            if direction in (1j, -1j)
            else [Beam(position, direction)],

        "-": lambda: [
                Beam(position, turn_left(direction)),
                Beam(position, turn_right(direction)),
            ]
            if direction in (1, -1)
            else [Beam(position, direction)],

        "/": lambda: [Beam(position, turn_left(direction))]
            if direction in (1j, -1j)
            else [Beam(position, turn_right(direction))]
            if direction in (-1, 1)
            else [],

        "\\": lambda: [Beam(position, turn_right(direction))]
            if direction in (1j, -1j)
            else [Beam(position, turn_left(direction))]
            if direction in (-1, 1)
            else [],
    }

    return beam_generators.get(tile, list)()
