from .card_representations import ascii_representation, hidden_ascii_representation
import random


class Card:
    rank_value = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14
    }

    suit_ascii = {
        "spades": ('♠', 0),
        "hearts": ('♥', 1),
        "diamonds": ('♦', 4),
        "clubs": ('♣', 2)
    }

    def __init__(self, rank: str = None, suit: str = None):
        self.rank = rank
        self.value = self.rank_value[rank] if rank else None
        self.suit = suit
        self.visible = (rank is not None and suit is not None)

    def color(self) -> int:
        return self.suit_ascii[self.suit][1]

    def to_array(self) -> list:
        return [self.rank, self.suit]

    # Prints the visual representation of the card, for curses graphics
    def to_ascii(self) -> str:
        if self.visible:
            return ascii_representation(self.rank,
                                        self.suit_ascii[self.suit][0])
        return hidden_ascii_representation()

    def is_playable(self, hand, led_card):
        # leading?
        if not led_card:
            return True
        # following suit?
        if self.suit == led_card.suit:
            return True
        # capable of follwing suit?
        for card in hand:
            if card.suit == led_card.suit:
                return False

        return True

    # ABSOLUTELY NEED THIS FOR LIST MEMBERSHIP
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        return NotImplemented

    # Needed for hand sorting (i.e. organization)
    def __lt__(self, other):
        if isinstance(other, Card):
            if self.suit_ascii[self.suit][1] == self.suit_ascii[other.suit][1]:
                return self.value > other.value
            else:
                return self.suit_ascii[self.suit][1] > self.suit_ascii[
                    other.suit][1]
        return NotImplemented

    # Makes printing cards nice (for debugging)
    def __repr__(self):
        if self.rank and self.suit:
            return "{:s}{:s}".format(self.rank, self.suit_ascii[self.suit][0])
        else:
            return "xx"


class Deck:
    ranks = Card.rank_value.keys()
    suits = Card.suit_ascii.keys()

    def __init__(self):
        self.next_index = 0
        self.deck = [
            Card(rank, suit) for rank in self.ranks for suit in self.suits
        ]

    def shuffle(self):
        self.next_index = 0
        random.shuffle(self.deck)

    def next(self):
        # Can't deal a card if we're out of bounds
        if self.next_index == 52:
            return None
        card = self.deck[self.next_index]
        self.next_index += 1
        return card


def trick_value(card: list, trump_card: list, led_card: list):
    if trump_card is not None and card[1] == trump_card[1]:
        return 100 + Card.rank_value[card[0]]
    elif card[1] == led_card[1]:
        return Card.rank_value[card[0]]
    return 0
