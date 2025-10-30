#!/usr/bin/env python3

"""
Solves Project Euler Problem 206: Concealed Square

Problem: Find the unique positive integer whose square has the form
1_2_3_4_5_6_7_8_9_0.

Analysis:
1.  The square `n^2` ends in `0`. This implies `n` must end in `0`.
2.  If `n` ends in `0`, then `n^2` must end in `00`.
3.  This means the form is actually 1_2_3_4_5_6_7_8_900.
4.  Let `n = 10 * m`. Then `n^2 = 100 * m^2`.
5.  We are looking for an integer `m` such that `m^2` has the form
    1_2_3_4_5_6_7_8_9.
6.  The last digit of `m^2` is `9`. This implies `m` must end in `3` or `7`.
7.  We can determine the search range for `m` by taking the square root of
    the minimum and maximum possible numbers for `m^2`.
    - Min `m^2`: 10203040506070809 (all blanks are 0)
    - Max `m^2`: 19293949596979899 (all blanks are 9)
8.  `min_m = ceil(sqrt(10203040506070809))` = 101010101
    `max_m = floor(sqrt(19293949596979899))` = 138902663
9.  We only need to search for `m` in the range [101010101, 138902663]
    where `m` ends in `3` or `7`.
10. The first candidate in this range is 101010103.
11. The last candidate is 138902663.
"""


def solve():
    """
    Finds the integer by iterating through the valid search space.
    """

    # Start at the first number >= 101010101 ending in 3
    m = 101010103

    # The last number to check is 138902663
    end_m = 138902663

    # We will alternate adding 4 (to get from ...3 to ...7)
    # and 6 (to get from ...7 to ...3)
    increment = 4

    while m <= end_m:
        square = m * m

        # We check if m^2 matches the pattern 1_2_3_4_5_6_7_8_9
        # This is done using integer arithmetic, which is faster
        # than string conversion.
        # We check from right to left, as mismatches are more likely
        # at the lower digits.
        if (square % 10 == 9 and
                (square // 100) % 10 == 8 and
                (square // 10000) % 10 == 7 and
                (square // 1000000) % 10 == 6 and
                (square // 100000000) % 10 == 5 and
                (square // 10000000000) % 10 == 4 and
                (square // 1000000000000) % 10 == 3 and
                (square // 10000000000000) % 10 == 2 and
                (square // 10000000000000000) == 1):
            # We found the matching `m`.
            # The problem asks for `n`, which is 10 * m.
            print(m * 10)

            # The problem states it is a "unique" integer,
            # so we can stop.
            break

        m += increment
        # Toggle the increment between 4 and 6
        increment = 10 - increment


if __name__ == "__main__":
    solve()
