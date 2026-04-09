import sys
from collections import Counter

def parse_card(card_str):
    """Convert a card string like '5H' to (value, suit)."""
    value_str = card_str[0]
    suit = card_str[1]
    if value_str == 'T':
        value = 10
    elif value_str == 'J':
        value = 11
    elif value_str == 'Q':
        value = 12
    elif value_str == 'K':
        value = 13
    elif value_str == 'A':
        value = 14
    else:
        value = int(value_str)
    return value, suit

def hand_rank(cards):
    """
    Evaluate a poker hand and return a comparable tuple.
    Higher tuple means stronger hand.
    """
    values = sorted([v for v, _ in cards])
    suits = [s for _, s in cards]

    flush = len(set(suits)) == 1

    # Straight detection
    straight = False
    high_straight = 0
    unique_vals = set(values)
    if len(unique_vals) == 5:
        if values[-1] - values[0] == 4:
            straight = True
            high_straight = values[-1]
        elif values == [2, 3, 4, 5, 14]:   # Ace‑low straight
            straight = True
            high_straight = 5

    # Frequency of each value
    counter = Counter(values)
    # Sort by count descending, then by value descending
    sorted_counts = sorted(counter.items(), key=lambda x: (-x[1], -x[0]))

    # Hand type determination
    if straight and flush:
        # Royal flush?
        if values == [10, 11, 12, 13, 14]:
            return (9,)          # Royal flush
        else:
            return (8, high_straight)   # Straight flush

    # Four of a kind
    if sorted_counts[0][1] == 4:
        four_val = sorted_counts[0][0]
        kicker = sorted_counts[1][0]
        return (7, four_val, kicker)

    # Full house
    if sorted_counts[0][1] == 3 and sorted_counts[1][1] == 2:
        three_val = sorted_counts[0][0]
        pair_val = sorted_counts[1][0]
        return (6, three_val, pair_val)

    # Flush
    if flush:
        desc_vals = sorted(values, reverse=True)
        return (5,) + tuple(desc_vals)

    # Straight
    if straight:
        return (4, high_straight)

    # Three of a kind
    if sorted_counts[0][1] == 3:
        three_val = sorted_counts[0][0]
        kickers = sorted([v for v in values if v != three_val], reverse=True)
        return (3, three_val, kickers[0], kickers[1])

    # Two pairs
    if len(sorted_counts) >= 2 and sorted_counts[0][1] == 2 and sorted_counts[1][1] == 2:
        high_pair = max(sorted_counts[0][0], sorted_counts[1][0])
        low_pair = min(sorted_counts[0][0], sorted_counts[1][0])
        kicker = sorted_counts[2][0]
        return (2, high_pair, low_pair, kicker)

    # One pair
    if sorted_counts[0][1] == 2:
        pair_val = sorted_counts[0][0]
        kickers = sorted([v for v in values if v != pair_val], reverse=True)
        return (1, pair_val, kickers[0], kickers[1], kickers[2])

    # High card
    desc_vals = sorted(values, reverse=True)
    return (0,) + tuple(desc_vals)

def main():
    wins = 0
    with open('0054_poker.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            cards = line.split()
            player1 = [parse_card(c) for c in cards[:5]]
            player2 = [parse_card(c) for c in cards[5:]]
            rank1 = hand_rank(player1)
            rank2 = hand_rank(player2)
            if rank1 > rank2:
                wins += 1
    print(wins)

if __name__ == '__main__':
    main()