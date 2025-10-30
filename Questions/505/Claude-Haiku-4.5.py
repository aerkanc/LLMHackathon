#!/usr/bin/env python3

import sys

sys.setrecursionlimit(5000000)


def solve():
    MOD = 2 ** 60
    n = 10 ** 12

    # Use dictionary for caching with minimal overhead
    x_cache = {}
    y_cache = {}

    def x(k):
        """Compute x(k) = x sequence with modular arithmetic"""
        if k == 0:
            return 0
        if k == 1:
            return 1

        try:
            return x_cache[k]
        except KeyError:
            pass

        if k & 1:  # k is odd: x(2m+1) = (2*x(m) + 3*x(m//5)) mod 2^60
            m = k >> 1
            result = (2 * x(m) + 3 * x(m // 5)) % MOD
        else:  # k is even: x(2m) = (3*x(m) + 2*x(m//5)) mod 2^60
            m = k >> 1
            result = (3 * x(m) + 2 * x(m // 5)) % MOD

        x_cache[k] = result
        return result

    def y(k):
        """Compute y_n(k) where n = 10^12"""
        # Base case: k >= n means y(k) = x(k)
        if k >= n:
            return x(k)

        try:
            return y_cache[k]
        except KeyError:
            pass

        # Recursive case: y(k) = (2^60 - 1) - max(y(2k), y(2k+1))
        left = y(k << 1)  # y(2k)
        right = y((k << 1) | 1)  # y(2k+1)
        result = (MOD - 1) - max(left, right)

        y_cache[k] = result
        return result

    # Compute and print the answer
    answer = y(1)
    print(answer)


if __name__ == "__main__":
    solve()