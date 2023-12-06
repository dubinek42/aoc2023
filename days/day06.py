from functools import reduce


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
    return sum(1 for s in range(seconds + 1) if s * (seconds - s) > distance)
