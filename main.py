import importlib

import typer


def main(
        day: int = typer.Option(..., "--day", "-d"),
        part: int = typer.Option(0, "--part", "-p"),
        test: bool = typer.Option(False, "--test", "-t")
):
    try:
        package = importlib.import_module(f"days.day{day:02}")
        filename = f"input{day:02}_test.txt" if test else f"input{day:02}.txt"
        with open(f"inputs/{filename}", "r") as file:
            day_input = file.read()
        if part in (0, 1):
            print("Part 1:", package.part1(day_input))
        if part in (0, 2):
            print("Part 2:", package.part2(day_input))
    except (ModuleNotFoundError, AttributeError, FileNotFoundError) as exc:
        print(str(exc))


if __name__ == '__main__':
    typer.run(main)
