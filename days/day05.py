from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias


@dataclass
class Range:
    dst: int
    src: int
    range: int

    @property
    def left(self) -> int:
        return self.src

    @property
    def right(self) -> int:
        return self.src + self.range - 1

    @property
    def change(self) -> int:
        return self.dst - self.src


Map: TypeAlias = list[Range]
SeedRange: TypeAlias = list[int]


def parse_input(day_input: str) -> tuple[list[int], list[Map]]:
    first_section, *sections = day_input.split("\n\n")
    seeds = [int(seed) for seed in first_section.split(": ")[-1].split()]
    maps = []
    for section in sections:
        _, *ranges = section.splitlines()
        maps.append([Range(*[int(x) for x in r.split()]) for r in ranges])
    return seeds, maps


def seeds_to_ranges(seeds: list[int]) -> list[SeedRange]:
    """Example: [2, 4, 7, 3] -> [[2, 5], [7, 9]]"""
    numbers = iter(seeds)
    result = []
    for start, count in zip(numbers, numbers):
        result.append([start, start + count - 1])
    return result


def apply_map(number: int, ranges: Map) -> int:
    for r in ranges:
        if r.left <= number <= r.right:
            return number + r.change
    return number


def apply_map_to_all(numbers: list[int], ranges: Map) -> list[int]:
    return [apply_map(number, ranges) for number in numbers]


def slice_ranges_and_apply_change(seeds: SeedRange, ranges: Map) -> list[SeedRange]:
    position, upper_limit = seeds
    slices = []
    ranges.sort(key=lambda x: x.left)  # Sort ranges based on left values

    for r in ranges:
        if position > upper_limit:
            break
        if position < r.left:
            # Before current range, no changes applied
            slices.append([position, r.left - 1])
            position = r.left
        elif r.left <= position <= r.right:
            # Inside current range, apply change
            new_right = min(r.right, upper_limit)
            slices.append([position + r.change, new_right + r.change])
            position = new_right + 1

    # Add the remaining part outside the ranges
    if position <= upper_limit:
        slices.append([position, upper_limit])

    return sorted(slices)


def merge_slices(slices: list[SeedRange]) -> list[SeedRange]:
    """Merge consecutive range slices if there are any.

    Example:
        [[1, 19], [20, 25], [40, 50]] -> [[1, 25], [40, 50]]
    """
    slices = sorted(slices)
    result = []
    for i, current_slice in enumerate(slices):
        if i == 0:
            result.append(current_slice)
        else:
            previous_slice = result[-1]
            if current_slice[0] <= previous_slice[1] + 1:
                # Merge slices
                result[-1] = [
                    previous_slice[0],
                    max(previous_slice[1], current_slice[1]),
                ]
            else:
                # Add current slice to result
                result.append(current_slice)
    return result


def part1(day_input: str) -> int:
    seeds, maps = parse_input(day_input)
    for m in maps:
        seeds = apply_map_to_all(seeds, m)
    return min(seeds)


def part2(day_input: str) -> int:
    seeds, maps = parse_input(day_input)
    seed_ranges = seeds_to_ranges(seeds)
    for m in maps:
        seed_ranges = merge_slices(
            [r for s in seed_ranges for r in slice_ranges_and_apply_change(s, m)],
        )
    return seed_ranges[0][0]
