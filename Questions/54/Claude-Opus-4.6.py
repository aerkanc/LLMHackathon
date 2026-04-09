from collections import Counter

VALUE_MAP = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13,
             'A': 14}


def hand_rank(cards):
    values = sorted([VALUE_MAP[c[0]] for c in cards], reverse=True)
    suits = [c[1] for c in cards]
    counts = Counter(values)
    groups = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
    ranks = [v for v, c in groups]
    freqs = [c for v, c in groups]

    is_flush = len(set(suits)) == 1
    is_straight = (len(set(values)) == 5 and values[0] - values[4] == 4)
    if set(values) == {14, 2, 3, 4, 5}:
        is_straight = True
        ranks = [5, 4, 3, 2, 1]

    if is_straight and is_flush:
        if values[0] == 14 and values[1] == 13:
            return (9, ranks)
        return (8, ranks)
    if freqs == [4, 1]:
        return (7, ranks)
    if freqs == [3, 2]:
        return (6, ranks)
    if is_flush:
        return (5, values)
    if is_straight:
        return (4, ranks)
    if freqs == [3, 1, 1]:
        return (3, ranks)
    if freqs == [2, 2, 1]:
        return (2, ranks)
    if freqs == [2, 1, 1, 1]:
        return (1, ranks)
    return (0, values)


count = 0
with open("0054_poker.txt") as f:
    for line in f:
        cards = line.strip().split()
        p1 = cards[:5]
        p2 = cards[5:]
        if hand_rank(p1) > hand_rank(p2):
            count += 1

print(count)