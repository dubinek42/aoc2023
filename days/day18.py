import numpy as np

MOVES = {
    "L": lambda x, y: (x[0], x[1] - y),
    "R": lambda x, y: (x[0], x[1] + y),
    "U": lambda x, y: (x[0] - y, x[1]),
    "D": lambda x, y: (x[0] + y, x[1]),
}

# Sequence of directions and magnitudes
Digs = list[tuple[str, int]]


def part1(day_input: str) -> int:
    return _calculate_lava(_parse_input(day_input))


def part2(day_input: str) -> int:
    return _calculate_lava(_parse_input(day_input, brutal_mode=True))


def _parse_input(day_input: str, brutal_mode: bool = False) -> Digs:
    result = []
    for line in day_input.splitlines():
        if brutal_mode:
            instruction = line.split()[2]
            result.append(("RDLU"[int(instruction[-2])], int(instruction[2:7], 16)))
        else:
            instructions = line.split()
            result.append((instructions[0], int(instructions[1])))
    return result


def _get_polygon(digs: Digs) -> tuple[list[tuple[int, int]], int]:
    boundary_len = 0
    position = (0, 0)
    polygon = [position]
    for direction, magnitude in digs:
        position = MOVES[direction](position, magnitude)
        polygon.append(position)
        boundary_len += magnitude
    return polygon, boundary_len


def _shoelace(polygon: list[tuple[int, int]]) -> int:
    x, y = np.array(polygon).T
    return int(np.abs(np.sum(x[:-1] * y[1:] - x[1:] * y[:-1]) / 2))


def _calculate_lava(digs: Digs) -> int:
    polygon, boundary_len = _get_polygon(digs)
    return _shoelace(polygon) + boundary_len // 2 + 1
