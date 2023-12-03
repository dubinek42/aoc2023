from functools import reduce
from typing import Any

import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel

NUMS_DOT = "1234567890."
GEAR = "*"


class Number(BaseModel):
    value: int
    positions: list[tuple[int, int]]
    gear: tuple[int, int] | None = None


def find_numbers_in_line(line: list[str], line_id: int) -> list[Number]:
    acc, positions, result = [], [], []
    for i, char in enumerate(line):
        if char.isdigit():
            acc.append(char)
            positions.append((i, line_id))
        elif acc:
            number = Number(value=int("".join(acc)), positions=positions)
            result.append(number)
            acc, positions = [], []
    if acc:
        number = Number(value=int("".join(acc)), positions=positions)
        result.append(number)
    return result


def neighbor_values(
    position: tuple[int, int],
    schema: NDArray[Any],
) -> list[str]:
    x, y = position
    result = []
    for col in range(-1, 2):
        if not (0 <= x + col < len(schema[y])):
            continue
        for row in range(-1, 2):
            if not (0 <= y + row < len(schema)) or (col == 0 and row == 0):
                continue
            result.append(schema[row + y][col + x])
    return result


def all_neighbors(number: Number, schema: NDArray[Any]) -> list[str]:
    return [
        neighbor
        for position in number.positions
        for neighbor in neighbor_values(position, schema)
    ]


def all_neighbors2(number: Number, schema: NDArray[Any]) -> list[tuple[int, int]]:
    left = min(x[0] for x in number.positions)
    right = max(x[0] for x in number.positions)
    line = number.positions[0][1]
    result = []

    for row in range(line - 1, line + 2):
        if not (0 <= row < len(schema)):
            continue
        for col in range(left - 1, right + 2):
            if not (0 <= col < len(schema[row])) or (col, row) in number.positions:
                continue
            result.append((col, row))
    return result


def is_part(number: Number, schema: NDArray[Any]) -> bool:
    return any(x not in NUMS_DOT for x in all_neighbors(number, schema))


def find_gear(number: Number, schema: NDArray[Any]) -> Number:
    neihgbors = all_neighbors2(number, schema)
    for col, row in neihgbors:
        if schema[row][col] == GEAR:
            number.gear = (col, row)
    return number


def find_gears(schema: NDArray[Any]) -> dict[tuple[int, int], list[int]]:
    gears: dict[tuple[int, int], list[int]] = {}
    for number in get_numbers_from_schema(schema):
        find_gear(number, schema)
        if number.gear:
            gears[number.gear] = [*gears.get(number.gear, []), number.value]
    return gears


def get_numbers_from_schema(schema: NDArray[Any]) -> list[Number]:
    return [
        number
        for line_id, line in enumerate(schema)
        for number in find_numbers_in_line(line, line_id)
    ]


def part1(day_input: str) -> int:
    schema = np.array([list(x) for x in day_input.splitlines()])
    return sum(x.value for x in get_numbers_from_schema(schema) if is_part(x, schema))


def part2(day_input: str) -> int:
    schema = np.array([list(x) for x in day_input.splitlines()])
    gears = find_gears(schema)
    filtered_gears = [x for x in gears.values() if len(x) == 2]
    return sum(reduce(lambda x, y: x * y, gear) for gear in filtered_gears)
