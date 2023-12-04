from pydantic import BaseModel


class Card(BaseModel):
    win: list[int]
    my: list[int]

    @property
    def win_count(self) -> int:
        return len([x for x in self.my if x in self.win])


def parse_cards(day_input: str) -> list[Card]:
    card_lines = [x.split(": ", 1)[1].split(" | ") for x in day_input.splitlines()]
    return [
        Card(
            win=[int(x) for x in line[0].split()],
            my=[int(x) for x in line[1].split()],
        )
        for line in card_lines
    ]


def part1(day_input: str) -> int:
    return sum(
        2 ** (card.win_count - 1) for card in parse_cards(day_input) if card.win_count
    )


def part2(day_input: str) -> int:
    cards = parse_cards(day_input)
    copies = [1] * len(cards)
    for i, card in enumerate(cards):
        for to_copy in range(i + 1, min(i + card.win_count + 1, len(cards))):
            copies[to_copy] += copies[i]
    return sum(copies)
