import typer


def main(
    day: int = typer.Option(..., "--day", "-d"),
) -> None:
    day_number = f"{day:02}"
    skeleton = """def part1(day_input: str) -> int:
    return 0


def part2(day_input: str) -> int:
    return 0
"""
    with open(f"days/day{day_number}.py", "a") as file:
        file.write(skeleton)

    with open(f"inputs/input{day_number}.txt", "w") as file:
        file.write("")

    with open(f"inputs/input{day_number}_test.txt", "w") as file:
        file.write("")


if __name__ == "__main__":
    typer.run(main)
