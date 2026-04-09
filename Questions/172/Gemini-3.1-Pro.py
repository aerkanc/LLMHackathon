import math


def solve():
    # We choose the first digit (1-9), there are 9 symmetric choices.
    # We model starting with the digit '1'.
    # This means digit '1' can be used at most 2 more times in the remaining 17 positions.
    # Digits '0' and '2'-'9' can be used at most 3 times.
    max_counts = [3, 2, 3, 3, 3, 3, 3, 3, 3, 3]
    memo = {}

    def ways(idx, rem):
        """
        idx: current digit index (0 to 9)
        rem: remaining length of the number to fill
        """
        if rem == 0:
            return 1
        if idx == 10:
            return 0

        state = (idx, rem)
        if state in memo:
            return memo[state]

        total_ways = 0
        limit = min(max_counts[idx], rem)

        # Try using the current digit `c` times
        for c in range(limit + 1):
            # math.comb(rem, c) gives the number of ways to place these `c` identical
            # digits in the `rem` available positions.
            total_ways += math.comb(rem, c) * ways(idx + 1, rem - c)

        memo[state] = total_ways
        return total_ways

    # Multiply by 9 for the 9 possible starting digits (1 through 9)
    ans = 9 * ways(0, 17)
    print(ans)


if __name__ == '__main__':
    solve()