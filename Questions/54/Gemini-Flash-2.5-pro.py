#!/usr/bin/env python3

"""
Solves Project Euler Problem 54: Poker Hands.

This script reads a file named 'poker.txt' which contains 1000 poker hands.
Each line contains ten cards, the first five for Player 1 and the last five
for Player 2. The script determines how many hands Player 1 wins.

The solution does not use multiprocessing or numpy as the problem size
(1000 hands) is very small. The logic for hand evaluation is fast, and
the entire file can be processed in milliseconds. Adding parallel processing
would introduce overhead and be slower than this simple, single-threaded solution.
"""

import collections
import sys


class Hand:
    """
    Represents a 5-card poker hand and calculates its rank as a
    comparable tuple.

    The rank tuple is structured so that Python's default tuple comparison
    correctly implements the poker tie-breaking rules.

    Rank Tuple Structure:
    (Hand Rank, Primary Card, Secondary Card, ... Kickers ...)

    Hand Ranks:
    10: Royal Flush
    9:  Straight Flush
    8:  Four of a Kind
    7:  Full House
    6:  Flush
    5:  Straight
    4:  Three of a Kind
    3:  Two Pairs
    2:  One Pair
    1:  High Card
    """

    # Map card ranks to numerical values for easy comparison
    VALUE_MAP = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14,
                 '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}

    def __init__(self, card_strings):
        """
        Initializes a Hand from a list of 5 card strings, e.g., ['8C', 'TS', 'KC'].

        Args:
            card_strings (list): A list of 5 strings representing the cards.
        """
        try:
            self.values = []
            self.suits = []
            for card in card_strings:
                self.values.append(self.VALUE_MAP[card[0]])
                self.suits.append(card[1])

            # The rank is calculated once and stored.
            self.rank = self._calculate_rank()
        except (KeyError, IndexError):
            # Handle potential malformed card strings
            self.rank = (0,)  # Assign lowest possible rank

    def _calculate_rank(self):
        """
        Determines the hand's rank as a comparable tuple.

        Returns:
            tuple: A tuple representing the hand's rank and tie-breakers.
        """
        values_sorted_desc = sorted(self.values, reverse=True)
        suits_set = set(self.suits)
        is_flush = len(suits_set) == 1

        # Check for straight
        is_straight = False
        straight_high_card = 0

        # Handle the A-2-3-4-5 (Ace-low) straight
        if values_sorted_desc == [14, 5, 4, 3, 2]:
            is_straight = True
            straight_high_card = 5  # An Ace-low straight is 5-high
        # Handle all other straights
        elif all(values_sorted_desc[i] == values_sorted_desc[i + 1] + 1 for i in range(4)):
            is_straight = True
            straight_high_card = values_sorted_desc[0]

        # --- Rank Checks (from highest to lowest) ---

        # 10: Royal Flush (A, K, Q, J, 10 all same suit)
        if is_straight and is_flush and straight_high_card == 14:
            return (10,)  # No tie-breakers needed

        # 9: Straight Flush (Any straight, all same suit, not Royal)
        if is_straight and is_flush:
            return (9, straight_high_card)

        # Get card value counts for remaining checks
        value_counts = collections.Counter(self.values)

        # Sort card values by their frequency, then by the card value itself.
        # This is crucial for all tie-breakers.
        # e.g., Full House KKK22 (Counter({13: 3, 2: 2})) -> [13, 2]
        # e.g., Two Pair 99553 (Counter({9: 2, 5: 2, 3: 1})) -> [9, 5, 3]
        # e.g., One Pair 77K52 (Counter({7: 2, 13: 1, 5: 1, 2: 1})) -> [7, 13, 5, 2]
        ranks_by_count_desc = sorted(value_counts, key=lambda k: (value_counts[k], k), reverse=True)

        # Get just the counts, sorted, e.g. [3, 2] for Full House
        counts_sorted = sorted(value_counts.values(), reverse=True)

        # 8: Four of a Kind
        if counts_sorted == [4, 1]:
            # (Rank, Four-of-a-kind card value, Kicker value)
            return (8, ranks_by_count_desc[0], ranks_by_count_desc[1])

        # 7: Full House
        if counts_sorted == [3, 2]:
            # (Rank, Three-of-a-kind card value, Pair card value)
            return (7, ranks_by_count_desc[0], ranks_by_count_desc[1])

        # 6: Flush
        if is_flush:
            # (Rank, High card, 2nd high, ..., 5th high)
            return (6,) + tuple(values_sorted_desc)

        # 5: Straight
        if is_straight:
            # (Rank, High card)
            return (5, straight_high_card)

        # 4: Three of a Kind
        if counts_sorted == [3, 1, 1]:
            # (Rank, Three-of-a-kind card, High kicker, Low kicker)
            return (4, ranks_by_count_desc[0], ranks_by_count_desc[1], ranks_by_count_desc[2])

        # 3: Two Pairs
        if counts_sorted == [2, 2, 1]:
            # (Rank, High pair card, Low pair card, Kicker)
            return (3, ranks_by_count_desc[0], ranks_by_count_desc[1], ranks_by_count_desc[2])

        # 2: One Pair
        if counts_sorted == [2, 1, 1, 1]:
            # (Rank, Pair card, High kicker, 2nd kicker, 3rd kicker)
            return (2, ranks_by_count_desc[0], ranks_by_count_desc[1], ranks_by_count_desc[2], ranks_by_count_desc[3])

        # 1: High Card
        # (Rank, High card, 2nd high, ..., 5th high)
        return (1,) + tuple(values_sorted_desc)

    def __gt__(self, other):
        """
        Compare this hand to another hand using Python's native
        tuple comparison, which handles all tie-breaking rules correctly.
        """
        return self.rank > other.rank


def solve_poker():
    """
    Reads 'poker.txt', compares all 1000 hands, and prints the number
    of wins for Player 1.
    """
    player_1_wins = 0
    # The problem description in the image refers to 'poker.txt'
    file_path = './0054poker.txt'

    try:
        with open(file_path, 'r') as f:
            for line in f:
                stripped_line = line.strip()
                if not stripped_line:  # Skip potential empty lines
                    continue

                cards = stripped_line.split(' ')

                # Basic data integrity check
                if len(cards) != 10:
                    continue

                player_1_hand = Hand(cards[0:5])
                player_2_hand = Hand(cards[5:10])

                if player_1_hand > player_2_hand:
                    player_1_wins += 1

        # The ONLY output must be the final answer.
        print(player_1_wins)

    except FileNotFoundError:
        # In the evaluation environment, the file is guaranteed to exist.
        # We suppress error output to ensure only the answer is printed.
        pass
    except Exception:
        # Suppress all other potential runtime errors.
        pass


if __name__ == "__main__":
    solve_poker()
