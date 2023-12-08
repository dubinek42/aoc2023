import math
from functools import reduce


def parse_input(day_input: str) -> tuple[str, dict[str, tuple[str, ...]]]:
    instructions, lines = day_input.split("\n\n")
    network = {}
    for line in lines.splitlines():
        key, value = line.split(" = ")
        network[key] = tuple(v.strip("()") for v in value.split(", "))
    return instructions, network


def big_lcm(x: int, y: int) -> int:
    """Support bigger numbers than math.lcm()."""
    return x * y // math.gcd(x, y)


def part1(day_input: str) -> int:
    instructions, network = parse_input(day_input)

    current_instruction = 0
    current_node = "AAA"
    steps = 0
    while current_node != "ZZZ":
        if current_instruction >= len(instructions):
            current_instruction = 0
        current_node = network[current_node][
            "LR".index(instructions[current_instruction])
        ]
        current_instruction += 1
        steps += 1

    return steps


def part2(day_input: str) -> int:
    instructions, network = parse_input(day_input)

    a_nodes = [x for x in network if x.endswith("A")]
    repeat_points = []
    for i in range(len(a_nodes)):
        current_instruction = 0
        steps = 0
        current_node = a_nodes[i]
        while steps < 100000:
            if current_instruction >= len(instructions):
                current_instruction = 0
            current_node = network[current_node][
                "LR".index(instructions[current_instruction])
            ]
            current_instruction += 1
            steps += 1
            if current_node.endswith("Z"):
                repeat_points.append(steps)
                break

    return reduce(big_lcm, repeat_points)
