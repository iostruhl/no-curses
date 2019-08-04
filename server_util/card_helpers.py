rank_value = {
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "10": 9,
    "J": 10,
    "Q": 11,
    "K": 12,
    "A": 13,
}


def trick_value(card: list, trump_card: list, led_card: list):
    if trump_card is not None and card[1] == trump_card[1]:
        return 100 + rank_value[card[0]]
    elif card[1] == led_card[1]:
        return rank_value[card[0]]
    return 0
