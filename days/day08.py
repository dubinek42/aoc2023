import math


def parse_input(day_input: str) -> tuple[str, dict[str, tuple[str, ...]]]:
    instructions, lines = day_input.split("\n\n")
    network = {}
    for line in lines.splitlines():
        key, value = line.split(" = ")
        network[key] = tuple(v.strip("()") for v in value.split(", "))
    return instructions, network


def part1(day_input: str) -> int:
    instructions, network = parse_input(day_input)

    steps = 0
    current_node = "AAA"
    while current_node != "ZZZ":
        current_instruction = steps % len(instructions)
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
    for node in a_nodes:
        steps = 0
        current_node = node
        while not current_node.endswith("Z"):
            current_instruction = steps % len(instructions)
            current_node = network[current_node][
                "LR".index(instructions[current_instruction])
            ]
            current_instruction += 1
            steps += 1
        repeat_points.append(steps)

    return math.lcm(*repeat_points)
