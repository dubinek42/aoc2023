import re

THashMap = dict[int, list[tuple[str, int]]]


def part1(day_input: str) -> int:
    return sum(_hash(s) for s in day_input.split(","))


def part2(day_input: str) -> int:
    hashmap = _build_hashmap(day_input)
    return sum(
        (box + 1) * (i + 1) * flength
        for box, lenses in hashmap.items()
        for i, (label, flength) in enumerate(lenses)
    )


def _hash(s: str) -> int:
    result = 0
    for c in s:
        result = ((result + ord(c)) * 17) % 256
    return result


def _build_hashmap(day_input: str) -> THashMap:
    hashmap: THashMap = {}
    for s in day_input.split(","):
        match = re.match(r"(\w*)([=-])(.*)", s)
        if not match:
            continue
        label = match.group(1)
        box = _hash(label)
        op = match.group(2)
        if op == "-" and box in hashmap and any(x[0] == label for x in hashmap[box]):
            i = [x[0] for x in hashmap[box]].index(label)
            del hashmap[box][i]
        if op == "=":
            flength = int(match.group(3))
            if box in hashmap:
                if any(x[0] == label for x in hashmap[box]):
                    i = [x[0] for x in hashmap[box]].index(label)
                    hashmap[box][i] = (label, flength)
                else:
                    hashmap[box].append((label, flength))
            else:
                hashmap[box] = [(label, flength)]
    return hashmap
