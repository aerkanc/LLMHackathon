from collections import Counter

def card_value(c):
    ranks = '23456789TJQKA'
    return ranks.index(c[0]) + 2  # 2..14
def is_straight(vals):
    v = sorted(set(vals))
    if len(v) != 5:
        return False, None
    # normal straight
    if v[-1] - v[0] == 4:
        return True, v[-1]
    # wheel straight A-2-3-4-5
    if v == [2,3,4,5,14]:
        return True, 5
    return False, None

def hand_rank(cards):
    vals = [card_value(c) for c in cards]
    suits = [c[1] for c in cards]
    flush = len(set(suits)) == 1
    straight, high_st = is_straight(vals)

    counts = Counter(vals)
    # sort by (count desc, value desc)
    groups = sorted(((cnt, v) for v, cnt in counts.items()), reverse=True)
    # unpack most common groups
    counts_sorted = [cnt for cnt, v in groups]
    values_sorted = [v for cnt, v in groups]

    if straight and flush:
        return (8, high_st)
    if counts_sorted == [4,1]:
        four = values_sorted[0]; kicker = values_sorted[1]
        return (7, four, kicker)
    if counts_sorted == [3,2]:
        return (6, values_sorted[0], values_sorted[1])
    if flush:
        return (5, sorted(vals, reverse=True))
    if straight:
        return (4, high_st)
    if counts_sorted == [3,1,1]:
        trip = values_sorted[0]
        kickers = sorted(values_sorted[1:], reverse=True)
        return (3, trip, kickers)
    if counts_sorted == [2,2,1]:
        pair_high, pair_low = sorted(values_sorted[:2], reverse=True)
        kicker = values_sorted[2]
        return (2, pair_high, pair_low, kicker)
    if counts_sorted == [2,1,1,1]:
        pair = values_sorted[0]
        kickers = sorted(values_sorted[1:], reverse=True)
        return (1, pair, kickers)
    return (0, sorted(vals, reverse=True))

def compare(p1, p2):
    return hand_rank(p1) > hand_rank(p2)

def main():
    wins = 0
    with open("./0054_poker.txt", "r") as f:
        for line in f:
            cards = line.strip().split()
            if len(cards) != 10:
                continue
            p1 = cards[:5]
            p2 = cards[5:]
            if compare(p1, p2):
                wins += 1
    print(wins)

if __name__ == "__main__":
    main()
