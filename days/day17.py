import heapq
from dataclasses import dataclass


@dataclass(eq=True, order=True, frozen=True)
class Item:
    cost: int
    position: tuple[float, float]
    direction: tuple[float, float]


def part1(day_input: str) -> int:
    heat_map, end = _parse_input(day_input)
    return _search(heat_map, 0, end)


def part2(day_input: str) -> int:
    heat_map, end = _parse_input(day_input)
    return _search(heat_map, 0, end, 4, 11)


def _parse_input(day: str) -> tuple[dict[complex, int], complex]:
    heat_map = {}
    position = complex(0)
    for line_number, line in enumerate(day.splitlines()):
        for c, char in enumerate(line):
            position = c + line_number * 1j
            heat_map[position] = int(char)
    return heat_map, position


def _search(
    graph: dict[complex, int],
    start: complex,
    end: complex,
    smallest: int = 0,
    largest: int = 4,
) -> int:
    q: list[Item] = []
    costs: dict[tuple[complex, complex], int] = {}
    for direction in (1, 1j, -1, -1j):
        heapq.heappush(
            q,
            Item(0, (start.real, start.imag), (direction.real, direction.imag)),
        )
    while q:
        item: Item = heapq.heappop(q)
        position = complex(*item.position)
        direction = complex(*item.direction)
        if (position, direction) in costs and costs[(position, direction)] <= item.cost:
            continue
        if position == end:
            return item.cost
        costs[(position, direction)] = item.cost
        for turn in (1j, -1j):
            new_direction = direction * turn
            new_position = position
            new_cost = item.cost
            for i in range(1, largest):
                new_position = new_position + new_direction
                if new_position not in graph:
                    break
                new_cost = new_cost + graph[new_position]
                if i >= smallest:
                    heapq.heappush(
                        q,
                        Item(
                            new_cost,
                            (new_position.real, new_position.imag),
                            (new_direction.real, new_direction.imag),
                        ),
                    )
    return 0
