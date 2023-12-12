from operator import add, sub
from typing import Callable


def part1(day_input: str) -> int:
    return sum(_extrapolate(history, -1, add) for history in _parse_input(day_input))


def part2(day_input: str) -> int:
    return sum(_extrapolate(history, 0, sub) for history in _parse_input(day_input))


def _parse_input(day_input: str) -> list[list[int]]:
    return [[int(x) for x in history.split()] for history in day_input.splitlines()]


def _get_sequences(history: list[int]) -> list[list[int]]:
    sequences = [history]
    while any(x != 0 for x in sequences[-1]):
        sequence = sequences[-1]
        sequences.append(
            [sequence[i + 1] - sequence[i] for i in range(len(sequence) - 1)],
        )
    return sequences


def _extrapolate(
    history: list[int],
    position: int,
    operation: Callable[[int, int], int],
) -> int:
    sequences = _get_sequences(history)
    numbers = [x[position] for x in sequences[::-1]]
    previous_number = 0
    for n in numbers[1:]:
        previous_number = operation(n, previous_number)
    return previous_number
