import math
from decimal import Decimal, getcontext


def solve():
    # Set high precision for decimal calculations to ensure the 9 digits are perfectly accurate
    getcontext().prec = 50

    # Using Linearity of Expectation:
    # Let E be the expected number of distinct colours.
    # E = sum( P(colour i is present) ) for i = 1 to 7
    # Since the probabilities are symmetric, E = 7 * P(colour 1 is present)
    # P(colour 1 is present) = 1 - P(colour 1 is absent)

    # Total ways to choose 20 balls out of 70
    total_ways = Decimal(math.comb(70, 20))

    # Total ways to choose 20 balls out of the remaining 60 (i.e., avoiding colour 1 completely)
    ways_colour_absent = Decimal(math.comb(60, 20))

    # Probability that a specific colour is NOT in the 20 drawn balls
    prob_absent = ways_colour_absent / total_ways

    # Expected number of distinct colours
    expected_value = Decimal('7') * (Decimal('1') - prob_absent)

    # Output the result formatted to 9 decimal places
    print(f"{expected_value:.9f}")


if __name__ == '__main__':
    solve()