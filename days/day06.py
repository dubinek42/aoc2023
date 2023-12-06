from functools import reduce

from .utils import quadratic_equation


def part1(day_input: str) -> int:
    races = list(
        zip(
            *[
                [int(x) for x in line.split(":")[-1].split()]
                for line in day_input.splitlines()
            ],
        ),
    )
    return reduce(
        lambda x, y: x * y,
        [
            sum(1 for s in range(race[0] + 1) if (race[0] - s) * s > race[1])
            for race in races
        ],
    )


def part2(day_input: str) -> int:
    seconds, distance = (
        int(x.split(":")[-1].replace(" ", "")) for x in day_input.splitlines()
    )
    return part2_quadratic(seconds, distance)  # This is the faster solution
    # This is the naive solution:
    # return sum(1 for s in range(seconds + 1) if s * (seconds - s) > distance)


def part2_quadratic(seconds: int, distance: int) -> int:
    x1, x2 = quadratic_equation(-1, seconds, -distance)
    return int(((x2 + (x2 % 2)) // 2) - ((x1 - (x1 % 2)) // 2) - 1)
