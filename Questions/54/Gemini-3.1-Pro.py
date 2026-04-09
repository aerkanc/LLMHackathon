import urllib.request
import os
import multiprocessing


def evaluate(hand):
    """
    Evaluates a poker hand and returns a tuple representing its strength.
    Tuple comparison in Python will naturally handle tie-breaking rules.
    """
    value_dict = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                  '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    values = [value_dict[card[0]] for card in hand]
    suits = [card[1] for card in hand]

    counts = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1

    # Sort frequencies descending by count, then by card value
    count_val = sorted([(c, v) for v, c in counts.items()], reverse=True)

    is_flush = len(set(suits)) == 1
    sorted_vals = sorted(values, reverse=True)

    is_straight = False
    straight_high = 0
    if len(count_val) == 5:
        # Standard Straight
        if sorted_vals[0] - sorted_vals[4] == 4:
            is_straight = True
            straight_high = sorted_vals[0]
        # A-low Straight (A, 2, 3, 4, 5)
        elif sorted_vals == [14, 5, 4, 3, 2]:
            is_straight = True
            straight_high = 5

    # Return Tuples: (Hand Rank, Tie-breaker 1, Tie-breaker 2, ...)
    if is_straight and is_flush:
        return (8, straight_high)
    if count_val[0][0] == 4:
        # Four of a Kind
        return (7, count_val[0][1], count_val[1][1])
    if count_val[0][0] == 3 and count_val[1][0] == 2:
        # Full House
        return (6, count_val[0][1], count_val[1][1])
    if is_flush:
        # Flush
        return (5,) + tuple(sorted_vals)
    if is_straight:
        # Straight
        return (4, straight_high)
    if count_val[0][0] == 3:
        # Three of a Kind
        return (3, count_val[0][1], count_val[1][1], count_val[2][1])
    if count_val[0][0] == 2 and count_val[1][0] == 2:
        # Two Pairs
        return (2, count_val[0][1], count_val[1][1], count_val[2][1])
    if count_val[0][0] == 2:
        # One Pair
        return (1, count_val[0][1], count_val[1][1], count_val[2][1], count_val[3][1])

    # High Card
    return (0,) + tuple(sorted_vals)


def process_line(line):
    """
    Parses a line of 10 cards and returns 1 if Player 1 wins, else 0.
    """
    cards = line.strip().split()
    if not cards:
        return 0

    hand1 = cards[:5]
    hand2 = cards[5:]

    # Compare evaluating tuples
    if evaluate(hand1) > evaluate(hand2):
        return 1
    return 0


def main():
    # Retrieve dataset if it's missing in the working directory
    file_name = '0054_poker.txt'
    if not os.path.exists(file_name):
        url = 'https://projecteuler.net/project/resources/p054_poker.txt'
        urllib.request.urlretrieve(url, file_name)

    with open(file_name, 'r') as f:
        lines = f.readlines()

    # Compute using Multi-core Processing
    with multiprocessing.Pool() as pool:
        results = pool.map(process_line, lines)

    print(sum(results))


if __name__ == '__main__':
    main()