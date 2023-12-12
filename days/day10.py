from typing import Any

import numpy as np
from numpy.typing import NDArray

neighbors = {
    "left": lambda x: (x[0], x[1] - 1),
    "right": lambda x: (x[0], x[1] + 1),
    "up": lambda x: (x[0] - 1, x[1]),
    "down": lambda x: (x[0] + 1, x[1]),
}

directions = {
    "|": ("up", "down"),
    "-": ("left", "right"),
    "L": ("up", "right"),
    "J": ("up", "left"),
    "7": ("down", "left"),
    "F": ("down", "right"),
}

opposite = {
    "left": "right",
    "right": "left",
    "up": "down",
    "down": "up",
}


def part1(day_input: str) -> int:
    pipes = _get_pipe_map(day_input)
    start = _get_start_position(pipes)
    direction = _get_first_directions(start, pipes)[0]
    return len(_build_loop(pipes, start, direction)) // 2


def part2(day_input: str) -> int:
    pipes = _get_pipe_map(day_input)
    start = _get_start_position(pipes)
    can_go = _get_first_directions(start, pipes)
    start_symbol = _get_start_symbol(can_go)
    loop = _build_loop(pipes, start, can_go[0])
    return _count_inside(pipes, start_symbol, loop)


def _get_pipe_map(day_input: str) -> NDArray[Any]:
    return np.array([list(x) for x in day_input.splitlines()])


def _get_first_directions(start: tuple[int, int], pipes: NDArray[Any]) -> list[str]:
    valid_pipes = {
        "left": ["-", "L", "F"],
        "right": ["-", "J", "7"],
        "up": ["|", "7", "F"],
        "down": ["|", "J", "L"],
    }
    return [
        direction
        for direction, neighbor in neighbors.items()
        if pipes[neighbor(start)] in valid_pipes[direction]
    ]


def _get_start_position(pipes: NDArray[Any]) -> tuple[int, int]:
    return tuple(np.argwhere(pipes == "S")[0])


def _get_start_symbol(can_go: list[str]) -> str:
    for pipe, dirs in directions.items():
        if dirs in (tuple(can_go), tuple(can_go[::-1])):
            return pipe
    raise ValueError


def _build_loop(
    pipes: NDArray[Any],
    start: tuple[int, int],
    can_go: str,
) -> list[tuple[int, int]]:
    position = start
    loop = [position]
    while True:
        position = neighbors[can_go](position)
        symbol = pipes[position]
        loop.append(position)
        if symbol == "S":
            break
        can_go = next(x for x in directions[symbol] if x != opposite[can_go])
    return loop


def _count_inside(
    pipes: NDArray[Any],
    start_symbol: str,
    loop: list[tuple[int, int]],
) -> int:
    count = 0
    downfacing_symbols = ["F", "7", "|"]
    if start_symbol in downfacing_symbols:
        downfacing_symbols.append("S")

    for row in range(len(pipes)):
        out = True
        for col in range(len(pipes[row])):
            if (row, col) in loop:
                if pipes[row, col] in downfacing_symbols:
                    out = not out
            elif not out:
                count += 1
    return count
