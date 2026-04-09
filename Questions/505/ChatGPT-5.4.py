M = 1 << 60
MASK = M - 1

def x_value(n: int) -> int:
    if n == 0:
        return 0
    a, b = 1, 0  # state for n = 1
    for ch in bin(n)[3:]:  # skip leading "0b1"
        if ch == '0':
            a, b = (3 * a + 2 * b) & MASK, a
        else:
            a, b = (2 * a + 3 * b) & MASK, a
    return a

def complete_descendant(k: int, d: int) -> int:
    # For a complete subtree of depth d, optimal path bits are:
    # 0, 10, 010, 1010, 01010, ...
    for rem in range(d, 0, -1):
        k = (k << 1) | (1 if rem % 2 == 0 else 0)
    return k

def solve(n: int) -> int:
    memo = {}

    def rec(k: int):
        if k in memo:
            return memo[k]

        if k >= n:
            memo[k] = (1, k)   # +1 means value is x(t)
            return memo[k]

        # Smallest d such that k * 2^d >= n
        d = max(1, (n - 1).bit_length() - k.bit_length())
        while (k << d) < n:
            d += 1
        while d > 0 and (k << (d - 1)) >= n:
            d -= 1

        # If the frontier inside subtree k is a complete binary tree of depth d,
        # collapse it directly.
        if d > 0 and ((k + 1) << (d - 1)) <= n:
            t = complete_descendant(k, d)
            memo[k] = (1 if d % 2 == 0 else -1, t)
            return memo[k]

        s1, t1 = rec(k << 1)
        s2, t2 = rec((k << 1) | 1)

        x1 = x_value(t1)
        x2 = x_value(t2)

        v1 = x1 if s1 > 0 else MASK - x1
        v2 = x2 if s2 > 0 else MASK - x2

        if v1 >= v2:
            memo[k] = (-s1, t1)
        else:
            memo[k] = (-s2, t2)
        return memo[k]

    s, t = rec(1)
    xt = x_value(t)
    return xt if s > 0 else MASK - xt

print(solve(10**12))