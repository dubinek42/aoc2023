from functools import reduce

PART_ONE_CUBES = [12, 13, 14]
COLOR_MAPPING = {"red": 0, "green": 1, "blue": 2}


def parse_turn(turn: str) -> list[int]:
    result = [0, 0, 0]
    for entry in turn.split(", "):
        number, color = entry.split(" ")
        result[COLOR_MAPPING[color]] += int(number)

    return result


def compare_lists(l1: list[int], l2: list[int]) -> bool:
    return all(value <= l2[list_id] for list_id, value in enumerate(l1))


def find_min(turns: list[list[int]]) -> list[int]:
    return [max(colors) for colors in zip(*turns)]


def part1(day_input: str) -> int:
    games = [line.split(": ")[1] for line in day_input.split("\n")]
    return sum(
        game_id + 1
        for game_id, game in enumerate(games)
        if all(compare_lists(parse_turn(x), PART_ONE_CUBES) for x in game.split("; "))
    )


def part2(day_input: str) -> int:
    games = [line.split(": ")[1] for line in day_input.split("\n")]
    return sum(
        reduce(
            lambda x, y: x * y,
            find_min(
                [parse_turn(x) for x in game.split("; ")],
            ),
        )
        for game in games
    )
