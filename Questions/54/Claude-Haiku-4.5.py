from collections import Counter

# Card value mapping
CARD_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13,
               'A': 14}
SUITS = {'C', 'D', 'H', 'S'}


def parse_card(card):
    """Convert card string like '8C' to (value, suit)"""
    return (CARD_VALUES[card[0]], card[1])


def evaluate_hand(cards):
    """
    Evaluate a 5-card poker hand.
    Returns a tuple (rank, tiebreakers) where rank is 0-9 and tiebreakers help break ties.
    Higher values indicate better hands.
    """
    parsed = [parse_card(card) for card in cards]
    values = sorted([v for v, s in parsed], reverse=True)
    suits = [s for v, s in parsed]

    # Count values
    value_counts = Counter(values)
    counts = sorted(value_counts.items(), key=lambda x: (x[1], x[0]), reverse=True)

    # Check for flush
    is_flush = len(set(suits)) == 1

    # Check for straight
    is_straight = False
    straight_high = 0
    sorted_values = sorted(set(values), reverse=True)
    if len(sorted_values) == 5:
        if sorted_values[0] - sorted_values[4] == 4:
            is_straight = True
            straight_high = sorted_values[0]
        # Check for A-2-3-4-5 (wheel/bicycle)
        elif sorted_values == [14, 5, 4, 3, 2]:
            is_straight = True
            straight_high = 5  # In this case, 5 is the high card

    # Determine hand rank and tiebreakers
    count_pattern = tuple(c[1] for c in counts)

    # Royal Flush: A-K-Q-J-T all same suit
    if is_flush and is_straight and straight_high == 14:
        return (9, (14,))  # Royal Flush

    # Straight Flush
    if is_flush and is_straight:
        return (8, (straight_high,))

    # Four of a Kind
    if count_pattern == (4, 1):
        quad_val = counts[0][0]
        kicker = counts[1][0]
        return (7, (quad_val, kicker))

    # Full House
    if count_pattern == (3, 2):
        trip_val = counts[0][0]
        pair_val = counts[1][0]
        return (6, (trip_val, pair_val))

    # Flush
    if is_flush:
        return (5, tuple(values))

    # Straight
    if is_straight:
        return (4, (straight_high,))

    # Three of a Kind
    if count_pattern == (3, 1, 1):
        trip_val = counts[0][0]
        kickers = tuple(sorted([counts[1][0], counts[2][0]], reverse=True))
        return (3, (trip_val,) + kickers)

    # Two Pair
    if count_pattern == (2, 2, 1):
        pairs = sorted([counts[0][0], counts[1][0]], reverse=True)
        kicker = counts[2][0]
        return (2, (pairs[0], pairs[1], kicker))

    # One Pair
    if count_pattern == (2, 1, 1, 1):
        pair_val = counts[0][0]
        kickers = tuple(sorted([counts[1][0], counts[2][0], counts[3][0]], reverse=True))
        return (1, (pair_val,) + kickers)

    # High Card
    return (0, tuple(values))


def compare_hands(hand1, hand2):
    """
    Compare two hands. Return True if hand1 wins, False if hand2 wins.
    """
    rank1, tie1 = evaluate_hand(hand1)
    rank2, tie2 = evaluate_hand(hand2)

    if rank1 != rank2:
        return rank1 > rank2

    # Same rank, compare tiebreakers
    return tie1 > tie2


def main():
    player1_wins = 0

    with open('./0054_poker.txt', 'r') as f:
        for line in f:
            cards = line.strip().split()
            if len(cards) != 10:
                continue

            player1_hand = cards[:5]
            player2_hand = cards[5:]

            if compare_hands(player1_hand, player2_hand):
                player1_wins += 1

    print(player1_wins)


if __name__ == '__main__':
    main()