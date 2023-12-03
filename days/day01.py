import re


NUMBERS = {"one": 1, "two": 2, "three": 3, "four": 4,
           "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}


def get_all_substrings(s: str) -> list[str]:
    return [s[i: j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)]


def replace_words(line: str) -> str:
    for substring in get_all_substrings(line):
        if substring in NUMBERS:
            line = line.replace(substring, substring[0] + str(NUMBERS[substring]) + substring[-1], 1)
            return replace_words(line)
    return line


def convert_line(line: str) -> int:
    line = replace_words(line)
    line = re.sub("[A-Za-z]", "", line)
    if len(line) > 0:
        return int(line[0] + line[-1])
    return 0


def part1(day_input: str) -> int:
    filtered = re.sub("[A-Za-z]", "", day_input)
    numbers = [int(x[0] + x[-1]) for x in filtered.split("\n") if len(x) > 0]
    return sum(numbers)


def part2(day_input: str) -> int:
    return sum(convert_line(line) for line in day_input.splitlines())
