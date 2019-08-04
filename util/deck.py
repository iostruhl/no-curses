import random


class Deck:
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suits = ["spades", "hearts", "diamonds", "clubs"]

    def __init__(self):
        self.next_index = 0
        self.deck = [[rank, suit] for rank in self.ranks
                     for suit in self.suits]

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
