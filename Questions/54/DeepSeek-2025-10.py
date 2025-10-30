import numpy as np
from multiprocessing import Pool


def card_value(card):
    """Convert card character to numerical value"""
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
              'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    return values[card[0]]


def card_suit(card):
    """Get card suit"""
    return card[1]


def evaluate_hand(hand):
    """Evaluate a poker hand and return a score tuple for comparison"""
    # Convert cards to numerical values and suits
    values = np.array([card_value(card) for card in hand])
    suits = [card_suit(card) for card in hand]

    # Sort values in descending order
    values_sorted = np.sort(values)[::-1]

    # Check for flush
    is_flush = len(set(suits)) == 1

    # Check for straight
    is_straight = True
    for i in range(1, 5):
        if values_sorted[i - 1] - values_sorted[i] != 1:
            is_straight = False
            break

    # Special case: Ace-low straight (A,2,3,4,5)
    if not is_straight and np.array_equal(values_sorted, [14, 5, 4, 3, 2]):
        is_straight = True
        values_sorted = np.array([5, 4, 3, 2, 1])  # Treat Ace as 1 for comparison

    # Count value frequencies
    unique, counts = np.unique(values, return_counts=True)
    count_dict = dict(zip(unique, counts))

    # Sort by frequency then value (for tie-breaking)
    sorted_by_freq = sorted(unique, key=lambda x: (-count_dict[x], -x))

    # Evaluate hand type
    if is_flush and is_straight:
        if values_sorted[0] == 14:  # Royal flush
            return (9, values_sorted[0])
        else:  # Straight flush
            return (8, values_sorted[0])

    if 4 in counts:  # Four of a kind
        four_of_kind = unique[np.where(counts == 4)[0][0]]
        kicker = unique[np.where(counts == 1)[0][0]]
        return (7, four_of_kind, kicker)

    if 3 in counts and 2 in counts:  # Full house
        three_of_kind = unique[np.where(counts == 3)[0][0]]
        pair = unique[np.where(counts == 2)[0][0]]
        return (6, three_of_kind, pair)

    if is_flush:  # Flush
        return (5,) + tuple(values_sorted)

    if is_straight:  # Straight
        return (4, values_sorted[0])

    if 3 in counts:  # Three of a kind
        three_of_kind = unique[np.where(counts == 3)[0][0]]
        kickers = sorted([v for v in unique if count_dict[v] == 1], reverse=True)
        return (3, three_of_kind, kickers[0], kickers[1])

    if np.sum(counts == 2) == 2:  # Two pairs
        pairs = sorted([v for v in unique if count_dict[v] == 2], reverse=True)
        kicker = [v for v in unique if count_dict[v] == 1][0]
        return (2, pairs[0], pairs[1], kicker)

    if 2 in counts:  # One pair
        pair = unique[np.where(counts == 2)[0][0]]
        kickers = sorted([v for v in unique if count_dict[v] == 1], reverse=True)
        return (1, pair, kickers[0], kickers[1], kickers[2])

    # High card
    return (0,) + tuple(values_sorted)


def process_line(line):
    """Process a single line of the poker file"""
    cards = line.strip().split()
    if len(cards) != 10:
        return 0

    player1_hand = cards[:5]
    player2_hand = cards[5:]

    player1_score = evaluate_hand(player1_hand)
    player2_score = evaluate_hand(player2_hand)

    # Compare scores lexicographically
    if player1_score > player2_score:
        return 1
    else:
        return 0


def main():
    # Read the file
    with open('./0054_poker.txt', 'r') as f:
        lines = f.readlines()

    # Use multiprocessing to process lines in parallel
    with Pool() as pool:
        results = pool.map(process_line, lines)

    # Sum up Player 1 wins
    player1_wins = sum(results)
    print(player1_wins)


if __name__ == '__main__':
    main()