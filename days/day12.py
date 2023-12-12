import functools

UNFOLD = 5


def part1(day_input: str) -> int:
    return sum(
        _combinations(springs, groups) for springs, groups in _parse_input(day_input)
    )


def part2(day_input: str) -> int:
    return sum(
        _combinations("?".join([springs] * UNFOLD), groups * UNFOLD)
        for springs, groups in _parse_input(day_input)
    )


def _parse_input(day_input: str) -> list[tuple[str, tuple[int, ...]]]:
    return [
        (springs, tuple(map(int, n.split(","))))
        for line in day_input.splitlines()
        for springs, n in [line.split()]
    ]


@functools.cache
def _combinations(springs: str, groups: tuple[int, ...]) -> int:
    if not groups:
        return 0 if "#" in springs else 1

    valid_combinations = 0

    first, *rest = groups
    for i in range(len(springs) - sum(rest) - first + 1):
        combination = "." * i + "#" * first + "."
        if _is_valid(springs, combination):
            valid_combinations += _combinations(
                springs[len(combination) :],
                tuple(rest),
            )

    return valid_combinations


def _is_valid(springs: str, combination: str) -> bool:
    for spring, possible_spring in zip(springs, combination):
        if spring != possible_spring and spring != "?":
            return False
    return True
