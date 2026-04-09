import sys

sys.setrecursionlimit(100000)

MOD = 1 << 60
N = 10**12

# Precompute coefficients L[t] and M[t] for t = 0 .. 60
T_MAX = 60
L = [(0, 0)] * (T_MAX + 1)
M_coeff = [(0, 0)] * (T_MAX + 1)
L[0] = (1, 0)
M_coeff[0] = (1, 0)

for t in range(1, T_MAX + 1):
    if t & 1:  # odd t
        c1, c2 = L[t - 1]
        L[t] = ((3 * c1 + c2) % MOD, (2 * c1) % MOD)
        M_coeff[t] = ((2 * c1 + c2) % MOD, (3 * c1) % MOD)
    else:      # even t
        c1, c2 = L[t - 1]
        L[t] = ((2 * c1 + c2) % MOD, (3 * c1) % MOD)
        M_coeff[t] = ((3 * c1 + c2) % MOD, (2 * c1) % MOD)

# Cache for x(k) and x(k>>1)
x_cache = {0: (0, 0), 1: (1, 0)}

def get_x_pair(k):
    """Return (x(k), x(k>>1)) modulo MOD."""
    if k in x_cache:
        return x_cache[k]
    # iterative construction from the second most significant bit
    a, b = 1, 0
    # get bits after the leading 1
    bit_len = k.bit_length()
    mask = 1 << (bit_len - 2)
    while mask:
        if k & mask:
            a, b = (2 * a + 3 * b) % MOD, a
        else:
            a, b = (3 * a + 2 * b) % MOD, a
        mask >>= 1
    x_cache[k] = (a, b)
    return a, b

def F(k, t):
    """Value of a full subtree with root k and t extra bits."""
    a, b = get_x_pair(k)
    if t % 2 == 0:   # even t -> direct value
        if a >= b:
            c1, c2 = L[t]
        else:
            c1, c2 = M_coeff[t]
        return (c1 * a + c2 * b) % MOD
    else:            # odd t -> value = complement of linear form
        if a >= b:
            c1, c2 = L[t]
        else:
            c1, c2 = M_coeff[t]
        linear = (c1 * a + c2 * b) % MOD
        return (MOD - 1 - linear) % MOD

memo_val = {}

def value(k):
    """Return y_n(k)."""
    if k in memo_val:
        return memo_val[k]
    if k >= N:
        a, _ = get_x_pair(k)
        res = a
    else:
        # find smallest t such that k*2^t >= N
        t = 0
        while (k << t) < N:
            t += 1
        # check if the whole subtree of depth t is a full leaf block
        if ((k + 1) << (t - 1)) <= N:
            res = F(k, t)
        else:
            left = value(2 * k)
            right = value(2 * k + 1)
            res = (MOD - 1 - max(left, right)) % MOD
    memo_val[k] = res
    return res

def solve():
    return value(1)

if __name__ == "__main__":
    print(solve())