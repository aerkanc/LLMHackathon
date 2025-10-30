import numpy as np
from math import comb


def solve():
    # DP state: (length, count0, count1, count2, count3)
    # where count_i = number of digits that have appeared exactly i times
    # We have 10 digits total: count0 + count1 + count2 + count3 = 10

    n = 18
    dp = np.zeros((n + 1, 11, 11, 11), dtype=np.int64)

    # Initial state: length 0, all 10 digits have appeared 0 times
    dp[0, 10, 0, 0] = 1

    for length in range(n):
        for c0 in range(11):
            for c1 in range(11 - c0):
                for c2 in range(11 - c0 - c1):
                    c3 = 10 - c0 - c1 - c2
                    if c3 < 0 or c3 > 10:
                        continue

                    current = dp[length, c0, c1, c2]
                    if current == 0:
                        continue

                    # We can choose digits that:
                    # - Haven't appeared before (from c0)
                    # - Have appeared once (from c1)
                    # - Have appeared twice (from c2)
                    # Cannot choose digits that have appeared 3 times (c3)

                    # Choose from digits that haven't appeared before
                    if c0 > 0:
                        ways = c0
                        # First digit cannot be 0, so if this is the first position,
                        # we can't choose digit 0 from the unused digits
                        if length == 0 and c0 > 0:
                            ways = c0 - 1  # exclude digit 0
                        if ways > 0:
                            dp[length + 1, c0 - 1, c1 + 1, c2] += current * ways

                    # Choose from digits that have appeared once
                    if c1 > 0:
                        dp[length + 1, c0, c1 - 1, c2 + 1] += current * c1

                    # Choose from digits that have appeared twice
                    if c2 > 0:
                        dp[length + 1, c0, c1, c2 - 1] += current * c2

    result = 0
    # Sum all states of length 18
    for c0 in range(11):
        for c1 in range(11 - c0):
            for c2 in range(11 - c0 - c1):
                c3 = 10 - c0 - c1 - c2
                if c3 >= 0:
                    result += dp[18, c0, c1, c2]

    print(result)


if __name__ == "__main__":
    solve()