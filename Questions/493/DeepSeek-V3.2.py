import math

def main():
    # Compute total number of ways to choose 20 balls from 70
    total = math.comb(70, 20)
    # Number of ways to choose 20 balls that avoid a specific colour (60 balls of other colours)
    no_colour = math.comb(60, 20)
    # Probability that a given colour is absent
    p_missing = no_colour / total
    # Expected number of distinct colours
    expected = 7.0 * (1.0 - p_missing)
    # Output with nine decimal places
    print("{:.9f}".format(expected))

if __name__ == "__main__":
    main()