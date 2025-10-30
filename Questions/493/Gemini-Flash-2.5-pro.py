def solve():
    """
    Computes the expected number of distinct colours.

    Let X be the random variable for the number of distinct colours.
    Let I_c be an indicator variable for colour c (c in {1, ..., 7}).
    I_c = 1 if colour c is present, 0 otherwise.

    X = I_1 + I_2 + ... + I_7

    By Linearity of Expectation:
    E[X] = E[I_1] + E[I_2] + ... + E[I_7]

    By symmetry, E[I_c] is the same for all colours.
    E[I_c] = P(I_c = 1)

    P(I_c = 1) = 1 - P(I_c = 0)

    P(I_c = 0) is the probability that no balls of colour c are picked.
    There are 70 balls total, 10 of colour c, 60 not of colour c.
    We pick 20 balls.

    Total ways to pick 20 from 70: C(70, 20)
    Ways to pick 20 from the 60 non-c balls: C(60, 20)

    P(I_c = 0) = C(60, 20) / C(70, 20)

    C(60, 20) / C(70, 20) = (60! / (20! * 40!)) / (70! / (20! * 50!))
                         = (60! * 50!) / (40! * 70!)
                         = (60 * 59 * ... * 41) / (70 * 69 * ... * 51)

    We can compute this as a product of 20 fractions:
    (60/70) * (59/69) * ... * (41/51)
    """

    # Calculate P(I_c = 0)
    prob_miss_one_color = 1.0
    for i in range(20):
        # We use floating point numbers for precision
        numerator = 60.0 - i
        denominator = 70.0 - i
        prob_miss_one_color *= (numerator / denominator)

    # P(I_c = 1) = 1 - P(I_c = 0)
    prob_hit_one_color = 1.0 - prob_miss_one_color

    # E[X] = 7 * E[I_c] = 7 * P(I_c = 1)
    expected_distinct_colors = 7.0 * prob_hit_one_color

    # Print the final answer with 9 decimal places
    print(f"{expected_distinct_colors:.9f}")


if __name__ == "__main__":
    solve()
