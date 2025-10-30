#!/usr/bin/env python3

import sys

def solve():
    """
    Solves Project Euler Problem 172.

    The problem asks for the number of 18-digit numbers (no leading zeros)
    where no digit appears more than three times.

    Let T be the set of all 18-digit *sequences* (allowing leading zeros)
    where each digit (0-9) appears at most 3 times.

    Let T_i be the subset of T containing sequences that start with digit i.

    The total number of sequences is |T| = |T_0| + |T_1| + ... + |T_9|.

    The number we are looking for is the count of valid 18-digit numbers
    (no leading zeros), which is:
    |T_1| + |T_2| + ... + |T_9| = |T| - |T_0|.

    Let's analyze T_0 and T_1:
    - T_0: Sequences starting with '0'. The 17-digit tail must be formed
      from digits {0...9} such that:
      - count(0) <= 2
      - count(i) <= 3 for i in {1...9}
    - T_1: Sequences starting with '1'. The 17-digit tail must be formed
      from digits {0...9} such that:
      - count(1) <= 2
      - count(i) <= 3 for i in {0, 2...9}

    By symmetry, the number of ways to form these 17-digit tails is
    identical. The calculation only depends on the *constraints* (one digit
    limited to 2, nine digits limited to 3), not the *value* of the digits.
    Therefore, |T_0| = |T_1| = ... = |T_9|.

    This means the total number of valid numbers is:
    |T| - |T_0| = 9 * |T_0|

    We can calculate |T_0| using dynamic programming.
    Let dp[i][j] be the number of sequences of length j using the first i
    digits (0, 1, ..., i-1) that satisfy our specific constraints for T_0:
    - count(0) <= 2
    - count(1...i-1) <= 3

    The transition is:
    dp[i][j] = sum(dp[i-1][j-k] * C(j, k))
    where:
    - k is the number of times we use digit (i-1).
    - C(j, k) is "j choose k", the number of ways to place k digits
      in a sequence of length j.
    - The range of k depends on the digit:
      - if (i-1) is 0, k is in {0, 1, 2} (max_count = 2)
      - if (i-1) > 0, k is in {0, 1, 2, 3} (max_count = 3)

    The final value for |T_0| will be dp[10][17].
    The answer to the problem is 9 * dp[10][17].
    """

    # We need to compute counts for 17-digit tails.
    # Total digits = 10 (0 through 9)
    # Max length = 17
    MAX_DIGITS = 10
    MAX_LEN = 17

    # 1. Precompute binomial coefficients (Combinations)
    # C[n][k] = nCk
    # We need up to C[17][k]
    C = [[0] * (MAX_LEN + 1) for _ in range(MAX_LEN + 1)]
    for n in range(MAX_LEN + 1):
        C[n][0] = 1
        for k in range(1, n + 1):
            C[n][k] = C[n-1][k-1] + C[n-1][k]

    # 2. Initialize DP table
    # dp[i][j] = # of sequences of length j using first i digits (0..i-1)
    #            with the T_0 constraints.
    # Dimensions: (MAX_DIGITS + 1) x (MAX_LEN + 1)
    dp = [[0] * (MAX_LEN + 1) for _ in range(MAX_DIGITS + 1)]

    # Base case: 1 way to form an empty sequence (length 0) with 0 digits
    dp[0][0] = 1

    # 3. Fill the DP table
    for i in range(1, MAX_DIGITS + 1):
        digit = i - 1  # current digit we are adding (0-indexed)

        # Set the max count constraint for this digit
        if digit == 0:
            max_k = 2  # count(0) <= 2
        else:
            max_k = 3  # count(1..9) <= 3

        for j in range(MAX_LEN + 1):  # For each possible length j
            if dp[i-1][j] == 0:
                # Optimization: if no ways to make length j with
                # previous digits, skip calculations.
                continue

            for k in range(max_k + 1):  # For each possible count k of digit
                if j + k <= MAX_LEN:
                    # We can form a sequence of length (j+k) by
                    # taking a sequence of length j (using digits 0..i-2)
                    # and adding k copies of digit (i-1).
                    # The number of ways to interleave them is C[j+k][k].
                    dp[i][j+k] += dp[i-1][j] * C[j+k][k]

    # 4. Get the result
    # |T_0| is the number of 17-digit sequences using all 10 digits
    # with our constraints.
    T_0 = dp[MAX_DIGITS][MAX_LEN]

    # The final answer is 9 * |T_0|
    final_answer = 9 * T_0

    # Print only the final answer
    print(final_answer)

if __name__ == "__main__":
    solve()
