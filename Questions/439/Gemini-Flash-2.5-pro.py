#!/usr/bin/env python3

import sys

# Increase recursion depth for deep recursive calls in summatory functions
try:
    sys.setrecursionlimit(5000)
except (OverflowError, ValueError):
    print("Could not set recursion depth, proceeding with default.", file=sys.stderr)

# --- Constants ---
N = 10 ** 11
MOD = 10 ** 9
# We need to compute D(n) = (T1+T2)/2.
# To do this modulo MOD, we compute T1 and T2 modulo 2*MOD,
# sum them, and then perform an exact integer division by 2.
# The result is then D(n) % MOD.
MOD_SUM = 2 * MOD
SQRT_N = int(N ** 0.5)  # 316227

# --- Caching ---
# We use dictionaries for memoization.
# @functools.lru_cache is not used to allow for explicit cache clearing
# and to handle the large number of potential states.
D_cache = {}
G_cache = {}

# --- Precomputed Sieve Data ---
# We will store mu(n), g(n) = n*mu(n), and G(n) = sum(g(i) for i=1..n)
mu_sieve = [0] * (SQRT_N + 1)
g_sieve = [0] * (SQRT_N + 1)
G_prefix_sieve = [0] * (SQRT_N + 1)


def g_sieve(limit):
    """
    Sieves Mobius function mu(n), g(n) = n*mu(n), and its prefix sum G(n).
    Runs in O(N log log N) time.
    """
    global mu_sieve, g_sieve, G_prefix_sieve

    is_prime = [True] * (limit + 1)
    primes = []
    mu_sieve[1] = 1
    is_prime[0] = is_prime[1] = False

    for i in range(2, limit + 1):
        if is_prime[i]:
            primes.append(i)
            mu_sieve[i] = -1

        for p in primes:
            if i * p > limit:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu_sieve[i * p] = 0
                break
            else:
                mu_sieve[i * p] = -mu_sieve[i]

    for i in range(1, limit + 1):
        g_sieve[i] = (i * mu_sieve[i]) % MOD_SUM
        G_prefix_sieve[i] = (G_prefix_sieve[i - 1] + g_sieve[i]) % MOD_SUM


def S2(n, mod):
    """
    Computes the sum of integers from 1 to n, modulo mod.
    S2(n) = n * (n + 1) / 2
    We perform the division before the modulo.
    """
    n1 = n
    n2 = n + 1
    if n1 % 2 == 0:
        n1 //= 2
    else:
        n2 //= 2
    return ((n1 % mod) * (n2 % mod)) % mod


def get_T(n, k, mod):
    """
    Computes T_k(n) = sum_{j=1..n} (floor(n/j))^k % mod
    This uses the "hyperbola method" trick and runs in O(sqrt(n)).
    """
    if n == 0:
        return 0

    n_0 = int(n ** 0.5)
    res = 0

    # Part 1: j from 1 to n_0
    for j in range(1, n_0 + 1):
        term = pow(n // j, k, mod)
        res = (res + term) % mod

    # Part 2: j from n_0 + 1 to n
    # We group by v = floor(n/j)
    v_max = n // (n_0 + 1)
    for v in range(1, v_max + 1):
        # Count how many j's have floor(n/j) = v
        # This is (n // v) - (n // (v + 1))
        count = (n // v - n // (v + 1)) % mod
        term_k = pow(v, k, mod)
        res = (res + term_k * count) % mod

    return res


def compute_D(n):
    """
    Computes D(n) = sum_{k=1..n} d(k) % MOD.
    Uses the identity D(n) = sum_{j=1..n} S2(floor(n/j))
                          = (T_1(n) + T_2(n)) / 2
    Computes modulo MOD_SUM, then divides by 2.
    """
    if n in D_cache:
        return D_cache[n]

    # Compute T1 and T2 modulo MOD_SUM
    t1 = get_T(n, 1, MOD_SUM)
    t2 = get_T(n, 2, MOD_SUM)

    total_sum = (t1 + t2) % MOD_SUM

    # (T1+T2) is always even, so this division is exact.
    res = total_sum // 2

    D_cache[n] = res
    return res


def get_G(n):
    """
    Computes G(n) = sum_{i=1..n} g(i) = sum_{i=1..n} i * mu(i) % MOD_SUM
    Uses recursive identity G(x) = 1 - sum_{d=2..x} d * G(floor(x/d))
    This runs in O(sqrt(n)) with memoization.
    """
    if n <= SQRT_N:
        return G_prefix_sieve[n]

    if n in G_cache:
        return G_cache[n]

    res = 1  # G(x) = 1 - ...
    j = 2
    while j <= n:
        v = n // j
        j_end = n // v

        # Sum of d from j to j_end
        sum_d = (S2(j_end, MOD_SUM) - S2(j - 1, MOD_SUM) + MOD_SUM) % MOD_SUM

        # Recursive call
        term = (get_G(v) * sum_d) % MOD_SUM

        res = (res - term + MOD_SUM) % MOD_SUM
        j = j_end + 1

    G_cache[n] = res
    return res


def solve():
    """
    Main solver function.
    Derivation:
    S(N) = sum_{i,j=1..N} sigma_1(i*j)
    Using identity sigma_1(ij) = sum_{g|gcd(i,j)} mu(g) * g * sigma_1(i/g) * sigma_1(j/g)
    S(N) = sum_{g=1..N} mu(g) * g * (sum_{a=1..floor(N/g)} sigma_1(a))^2
    Let D(n) = sum_{k=1..n} sigma_1(k)
    S(N) = sum_{g=1..N} mu(g) * g * (D(floor(N/g)))^2

    We split this sum at g = SQRT_N.
    """

    # 1. Precompute sieve data up to SQRT_N
    g_sieve(SQRT_N)

    S1 = 0
    # 2. Sum for g from 1 to SQRT_N
    for g in range(1, SQRT_N + 1):
        if mu_sieve[g] == 0:
            continue

        g_mod_M = g % MOD

        # This computes D(n) % MOD
        D_val = compute_D(N // g)
        D_sq = (D_val * D_val) % MOD

        term = (g_mod_M * D_sq) % MOD

        if mu_sieve[g] == 1:
            S1 = (S1 + term) % MOD
        else:  # mu_sieve[g] == -1
            S1 = (S1 - term + MOD) % MOD

    S2 = 0
    # 3. Sum for g from SQRT_N + 1 to N
    # We group by v = floor(N/g)
    v_max = N // (SQRT_N + 1)

    for v in range(1, v_max + 1):
        # This computes D(v) % MOD
        D_val = compute_D(v)
        D_sq = (D_val * D_val) % MOD

        # We need sum_{g=n_low+1..n_high} mu(g) * g
        n_low = N // (v + 1)
        n_high = N // v

        # get_G(n) computes sum % MOD_SUM
        g_sum_mod_SUM = (get_G(n_high) - get_G(n_low) + MOD_SUM) % MOD_SUM

        # We need the sum % MOD
        g_sum_mod_M = g_sum_mod_SUM % MOD

        term = (D_sq * g_sum_mod_M) % MOD
        S2 = (S2 + term) % MOD

    # 4. Final answer
    S = (S1 + S2) % MOD
    print(S)


if __name__ == "__main__":
    solve()
