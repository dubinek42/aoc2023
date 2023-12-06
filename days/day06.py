from functools import reduce


def part1(day_input: str) -> int:
    return reduce(
        lambda x, y: x * y,
        [
            len(
                list(
                    filter(
                        lambda x: x > race[1],
                        [(race[0] - s) * s for s in range(race[0] + 1)],
                    ),
                ),
            )
            for race in list(
                zip(
                    *[
                        [int(x) for x in line.split(":")[-1].split()]
                        for line in day_input.splitlines()
                    ],
                ),
            )
        ],
    )


def part2(day_input: str) -> int:
    seconds, distance = (
        int(x.split(":")[-1].replace(" ", "")) for x in day_input.splitlines()
    )
    return len(
        [s * (seconds - s) for s in range(seconds + 1) if s * (seconds - s) > distance],
    )
