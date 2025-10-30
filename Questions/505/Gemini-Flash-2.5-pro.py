import sys

# Increase recursion depth for deep recursive calls in get_x
sys.setrecursionlimit(2000)


def solve():
    """
    Solves Project Euler Problem 505.

    The problem asks to compute A(10^12), where A(n) = y_n(1).
    The definitions are:
    x(0) = 0
    x(1) = 1
    x(2k) = (3x(k) + 2x(floor(k/2))) mod 2^60
    x(2k+1) = (2x(k) + 3x(floor(k/2))) mod 2^60

    y_n(k) = x(k) if k >= n
    y_n(k) = 2^60 - 1 - max(y_n(2k), y_n(2k+1)) if k < n

    Let M = 2^60 and inv(v) = (M - 1 - v).

    Analysis of x(k):
    It can be proven by induction that x(k) >= x(floor(k/2)) for all k >= 1.
    This implies:
    max(x(2k), x(2k+1))
      = max(3x(k) + 2x(floor(k/2)), 2x(k) + 3x(floor(k/2)))
      = 3x(k) + 2x(floor(k/2))  (since x(k) >= x(floor(k/2)))
      = x(2k)

    Analysis of y_n(k):
    y_n(k) defines a min-max computation on a tree.
    The height of the computation for A(n) = y_n(1) is H(n) = floor(log2(n-1)) + 1.

    Let's test the examples:
    N = 4, H(4) = floor(log2(3)) + 1 = 2.
    A(4) = y_4(1) = inv(max(y_4(2), y_4(3)))
         = inv(max(inv(max(x(4),x(5))), inv(max(x(6),x(7)))))
         = inv(max(inv(x(4)), inv(x(6))))  (since x(k) >= x(k//2))
         = min(x(4), x(6)) = min(11, 8) = 8.
    The example gives A(4) = 8. This matches. We also see 8 = x(6).
    So for H(N) = 2, A(N) = x(N + N/2).

    N = 10, H(10) = floor(log2(9)) + 1 = 4.
    A(10) = y_10(1) = inv(max(y_10(2), y_10(3)))
    y_10(2) = inv(max(y_10(4), y_10(5)))
    y_10(3) = inv(max(y_10(6), y_10(7)))

    y_10(4) = inv(max(y_10(8), y_10(9)))
            = inv(max(inv(max(x(16),x(17))), inv(max(x(18),x(19)))))
            = min(x(16), x(18))
    y_10(5) = inv(max(x(10), x(11))) = inv(x(10))
    y_10(6) = inv(max(x(12), x(13))) = inv(x(12))
    y_10(7) = inv(max(x(14), x(15))) = inv(x(14))

    y_10(2) = inv(max(min(x(16), x(18)), inv(x(10))))
            = inv(max(min(139, 115), inv(33)))
            = inv(max(115, inv(33))) = inv(inv(33)) = 33 = x(10)

    y_10(3) = inv(max(inv(x(12)), inv(x(14)))) = min(x(12), x(14))
            = min(28, 25) = 25 = x(14)

    A(10) = inv(max(y_10(2), y_10(3))) = inv(max(x(10), x(14)))
          = inv(max(33, 25)) = inv(33) = inv(x(10)).
    The example gives A(10) = 2^60 - 34 = inv(33). This matches.

    Pattern:
    H(N) = height of the computation tree
    If H(N) % 4 == 2 (e.g., N=4, H=2; N=1000, H=10), A(N) = x(...)
    If H(N) % 4 == 0 (e.g., N=10, H=4), A(N) = inv(x(N))

    Let's check N = 10^12:
    N = 1,000,000,000,000
    log2(N-1) is approx 39.86. floor(log2(N-1)) = 39.
    H(10^12) = 39 + 1 = 40.
    Since 40 % 4 == 0, we apply the same pattern as N=10.
    A(10^12) = inv(x(10^12)).

    We need a fast way to compute x(N).
    """

    N = 10 ** 12
    MOD = 1 << 60

    # Memoization table for x(k)
    memo_x = {0: 0, 1: 1}

    def get_x(k):
        """
        Computes x(k) using memoization.
        This function is O(log k) because the number of
        unique subproblems k, k//2, k//4, ... is logarithmic.
        """
        if k in memo_x:
            return memo_x[k]

        # k is not in memo, so k >= 2
        m = k // 2

        # We need x(m) and x(m//2)
        x_m = get_x(m)
        x_m_half = get_x(m // 2)

        if k % 2 == 0:
            # k = 2m
            res = (3 * x_m + 2 * x_m_half) % MOD
        else:
            # k = 2m + 1
            res = (2 * x_m + 3 * x_m_half) % MOD

        memo_x[k] = res
        return res

    # Compute x(10^12)
    x_N = get_x(N)

    # Compute A(10^12) = inv(x(10^12))
    # inv(v) = 2^60 - 1 - v
    result = (MOD - 1 - x_N)

    # The problem asks to print only the final answer
    print(result)


if __name__ == "__main__":
    solve()
