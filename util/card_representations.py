rank_representation = dict()

rank_representation['A'] = (
    "┌─────────┐\n"
    "│A        │\n"
    "│x        │\n"
    "│    █    │\n"
    "│   █ █   │\n"
    "│    █    │\n"
    "│        x│\n"
    "│        A│\n"
    "└─────────┘")
rank_representation['2'] = (
    "┌─────────┐\n"
    "│2        │\n"
    "│x   x    │\n"
    "│         │\n"
    "│         │\n"
    "│         │\n"
    "│    x   x│\n"
    "│        2│\n"
    "└─────────┘")
rank_representation['3'] = (
    "┌─────────┐\n"
    "│3        │\n"
    "│x   x    │\n"
    "│         │\n"
    "│    x    │\n"
    "│         │\n"
    "│    x   x│\n"
    "│        3│\n"
    "└─────────┘")
rank_representation['4'] = (
    "┌─────────┐\n"
    "│4        │\n"
    "│x  x x   │\n"
    "│         │\n"
    "│         │\n"
    "│         │\n"
    "│   x x  x│\n"
    "│        4│\n"
    "└─────────┘")
rank_representation['5'] = (
    "┌─────────┐\n"
    "│5        │\n"
    "│x  x x   │\n"
    "│         │\n"
    "│    x    │\n"
    "│         │\n"
    "│   x x  x│\n"
    "│        5│\n"
    "└─────────┘")
rank_representation['6'] = (
    "┌─────────┐\n"
    "│6        │\n"
    "│x  x x   │\n"
    "│         │\n"
    "│   x x   │\n"
    "│         │\n"
    "│   x x  x│\n"
    "│        6│\n"
    "└─────────┘")
rank_representation['7'] = (
    "┌─────────┐\n"
    "│7        │\n"
    "│x  x x   │\n"
    "│         │\n"
    "│   x x   │\n"
    "│    x    │\n"
    "│   x x  x│\n"
    "│        7│\n"
    "└─────────┘")
rank_representation['8'] = (
    "┌─────────┐\n"
    "│8        │\n"
    "│x  x x   │\n"
    "│    x    │\n"
    "│   x x   │\n"
    "│    x    │\n"
    "│   x x  x│\n"
    "│        8│\n"
    "└─────────┘")
rank_representation['9'] = (
    "┌─────────┐\n"
    "│9        │\n"
    "│x  x x   │\n"
    "│   x x   │\n"
    "│    x    │\n"
    "│   x x   │\n"
    "│   x x  x│\n"
    "│        9│\n"
    "└─────────┘")
rank_representation['10'] = (
    "┌─────────┐\n"
    "│10       │\n"
    "│x  x x   │\n"
    "│   x x   │\n"
    "│   x x   │\n"
    "│   x x   │\n"
    "│   x x  x│\n"
    "│       10│\n"
    "└─────────┘")
rank_representation['J'] = (
    "┌─────────┐\n"
    "│J        │\n"
    "│x █████  │\n"
    "│    █    │\n"
    "│    █    │\n"
    "│  █ █    │\n"
    "│  ███   x│\n"
    "│        J│\n"
    "└─────────┘")
rank_representation['Q'] = (
    "┌─────────┐\n"
    "│Q        │\n"
    "│x  ███   │\n"
    "│  █   █  │\n"
    "│  █   █  │\n"
    "│  █  ██  │\n"
    "│   ██ █ x│\n"
    "│        Q│\n"
    "└─────────┘")
rank_representation['K'] = (
    "┌─────────┐\n"
    "│K        │\n"
    "│x █   █  │\n"
    "│  █  █   │\n"
    "│  █ █    │\n"
    "│  █  █   │\n"
    "│  █   █ x│\n"
    "│        K│\n"
    "└─────────┘")
rank_representation['H'] = (
    "┌─────────┐\n"
    "│░░░░░░░░░│\n"
    "│░░░░░░░░░│\n"
    "│░░░░░░░░░│\n"
    "│░░░░░░░░░│\n"
    "│░░░░░░░░░│\n"
    "│░░░░░░░░░│\n"
    "│░░░░░░░░░│\n"
    "└─────────┘")

def ascii_representation(rank: str, suit: str, visibile: bool):
    if not visibile:
        return rank_representation['H']
    else:
        return rank_representation[rank].replace("x", suit)