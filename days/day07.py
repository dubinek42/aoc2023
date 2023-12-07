from collections import Counter, namedtuple
from enum import Enum
from typing import Callable

CARD_STRENGTH = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
CARD_STRENGTH2 = ("J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A")

Game = namedtuple("Game", ["hand", "bid"])


class HandType(int, Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIRS = 3
    THREE = 4
    FULL_HOUSE = 5
    FOUR = 6
    FIVE = 7


def parse_games(day_input: str) -> list[Game]:
    return [Game(*g) for line in day_input.splitlines() if (g := line.split())]


def get_type(hand: str) -> HandType:
    counter = Counter(hand)
    type_map = {
        1: HandType.FIVE,
        2: HandType.FOUR if 4 in counter.values() else HandType.FULL_HOUSE,
        3: HandType.THREE if 3 in counter.values() else HandType.TWO_PAIRS,
        4: HandType.PAIR,
        5: HandType.HIGH_CARD,
    }
    return type_map.get(len(counter), HandType.HIGH_CARD)


def get_type_with_joker(hand: str) -> HandType:
    if "J" not in hand:
        return get_type(hand)
    return max([get_type(hand.replace("J", c)) for c in set(hand)])


def count_score(
    games: list[Game],
    strength: tuple[str, ...],
    type_fn: Callable[[str], HandType],
) -> int:
    sorted_games = sorted(
        games,
        key=lambda x: (type_fn(x.hand), [strength.index(j) for j in x.hand]),
    )
    result = []
    for i, game in enumerate(sorted_games):
        result.append((i + 1) * int(game.bid))
    return sum(result)


def part1(day_input: str) -> int:
    return count_score(parse_games(day_input), CARD_STRENGTH, get_type)


def part2(day_input: str) -> int:
    return count_score(parse_games(day_input), CARD_STRENGTH2, get_type_with_joker)
