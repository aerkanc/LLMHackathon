from collections import Counter
from pathlib import Path

VALUE_MAP = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

def hand_rank(cards):
    values = sorted((VALUE_MAP[c[0]] for c in cards), reverse=True)
    suits = [c[1] for c in cards]
    counts = Counter(values)

    # Sort by frequency first, then card value
    groups = sorted(((cnt, val) for val, cnt in counts.items()), reverse=True)
    ordered = [val for cnt, val in groups for _ in range(cnt)]

    is_flush = len(set(suits)) == 1
    unique_vals = sorted(set(values))
    is_straight = len(unique_vals) == 5 and unique_vals[-1] - unique_vals[0] == 4

    # Category order:
    # 8 Straight Flush, 7 Four of a Kind, 6 Full House, 5 Flush,
    # 4 Straight, 3 Three of a Kind, 2 Two Pairs, 1 One Pair, 0 High Card
    if is_straight and is_flush:
        return (8, max(values))
    if groups[0][0] == 4:
        return (7, ordered)
    if groups[0][0] == 3 and groups[1][0] == 2:
        return (6, ordered)
    if is_flush:
        return (5, values)
    if is_straight:
        return (4, max(values))
    if groups[0][0] == 3:
        return (3, ordered)
    if groups[0][0] == 2 and groups[1][0] == 2:
        return (2, ordered)
    if groups[0][0] == 2:
        return (1, ordered)
    return (0, values)

def find_poker_file():
    candidates = [
        Path("./0054_poker.txt")
    ]
    for p in candidates:
        if p is not None and p.is_file():
            return p

    for root in [Path("."), Path("/mnt/data")]:
        try:
            for p in root.rglob("poker.txt"):
                if p.is_file():
                    return p
        except Exception:
            pass
    raise FileNotFoundError("poker.txt not found")

def main():
    path = find_poker_file()
    wins = 0
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            cards = line.strip().split()
            if not cards:
                continue
            p1 = cards[:5]
            p2 = cards[5:]
            if hand_rank(p1) > hand_rank(p2):
                wins += 1
    print(wins)

if __name__ == "__main__":
    main()