from math import comb
from decimal import Decimal, getcontext, ROUND_HALF_UP

def main():
    # Set high precision for accurate decimal representation
    getcontext().prec = 50

    # Probability that a given color is NOT picked in 20 draws without replacement:
    # C(60, 20) / C(70, 20)  (choosing all 20 from the 60 balls of other colors)
    p_not = Decimal(comb(60, 20)) / Decimal(comb(70, 20))

    # Expected number of distinct colors = sum over 7 colors of P(color appears at least once)
    expected = Decimal(7) * (Decimal(1) - p_not)

    # Print with exactly nine digits after the decimal point
    print(expected.quantize(Decimal('0.000000000'), rounding=ROUND_HALF_UP))

if __name__ == "__main__":
    main()
