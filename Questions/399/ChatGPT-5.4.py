import math
import sys
from collections import defaultdict

LAST16_MOD = 10**16
TARGET = 100_000_000
NMAX = 200_000_000  # hedef için yeterli üst sınır


def fib_mod(n: int, mod: int) -> int:
    """F_n mod mod, fast doubling."""
    a, b = 0, 1
    for bit in range(n.bit_length() - 1, -1, -1):
        c = (a * ((b << 1) - a)) % mod
        d = (a * a + b * b) % mod
        if (n >> bit) & 1:
            a, b = d, (c + d) % mod
        else:
            a, b = c, d
    return a


def sieve_primes(n: int) -> list[int]:
    if n < 2:
        return []
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    r = int(n ** 0.5)
    for p in range(2, r + 1):
        if sieve[p]:
            start = p * p
            sieve[start:n + 1:p] = b"\x00" * (((n - start) // p) + 1)
    return [i for i in range(2, n + 1) if sieve[i]]


def unique_prime_factors(n: int, small_primes: list[int]) -> list[int]:
    out = []
    x = n
    for p in small_primes:
        if p * p > x:
            break
        if x % p == 0:
            out.append(p)
            while x % p == 0:
                x //= p
    if x > 1:
        out.append(x)
    return out


def rank_of_apparition_prime(p: int, small_primes: list[int]) -> int:
    """
    z(p): smallest n >= 1 with p | F_n.
    For odd prime p != 5, z(p) divides p - (5/p).
    """
    if p == 2:
        return 3
    if p == 5:
        return 5

    leg = 1 if pow(5, (p - 1) // 2, p) == 1 else -1
    candidate = p - 1 if leg == 1 else p + 1
    z = candidate

    for q in unique_prime_factors(candidate, small_primes):
        while z % q == 0 and fib_mod(z // q, p) == 0:
            z //= q
    return z


def prime_upper_bound_for_moduli(nmax: int) -> int:
    """
    If p*z(p) <= nmax and z(p)=k, then p divides F_k and p <= nmax/k.
    We scan small k and maximize min(F_k, nmax/k) to get a safe prime bound.
    """
    a, b = 0, 1
    best = 0
    for k in range(1, 220):
        a, b = b, a + b  # F_k
        best = max(best, min(a, nmax // k))
        if k > 60 and (nmax // k) <= best:
            break
    return best


def build_forbidden_moduli(nmax: int) -> list[int]:
    """
    Build moduli m_p = p * z(p) <= nmax.
    Then discard redundant ones that are multiples of an already smaller modulus.
    """
    pmax = prime_upper_bound_for_moduli(nmax)
    primes = sieve_primes(pmax)
    small_primes = sieve_primes(int((pmax + 1) ** 0.5) + 1)

    mods = []
    for p in primes:
        z = rank_of_apparition_prime(p, small_primes)
        m = p * z
        if m <= nmax:
            mods.append(m)

    mods.sort()

    filtered = []
    for m in mods:
        redundant = False
        for f in filtered:
            if m % f == 0:
                redundant = True
                break
        if not redundant:
            filtered.append(m)

    return filtered


def build_inclusion_exclusion(mods: list[int], nmax: int):
    """
    Count good indices by inclusion-exclusion over forbidden divisibility moduli.

    good(N) = sum coeff[L] * floor(N / L),
    where coeff[L] is the accumulated IE coefficient for lcm == L.
    """
    coeff = defaultdict(int)
    coeff[1] = 1

    mods = [m for m in mods if m <= nmax]
    sys.setrecursionlimit(10000)

    def dfs(start: int, current_lcm: int, sign: int):
        for i in range(start, len(mods)):
            m = mods[i]
            if current_lcm % m == 0:
                continue
            nl = (current_lcm // math.gcd(current_lcm, m)) * m
            if nl > nmax:
                continue
            coeff[nl] -= sign
            dfs(i + 1, nl, -sign)

    dfs(0, 1, 1)

    items = sorted(coeff.items())
    lcms = [x for x, _ in items]
    coefs = [c for _, c in items]
    return lcms, coefs


def count_good_indices_upto(n: int, lcms: list[int], coefs: list[int]) -> int:
    total = 0
    for L, c in zip(lcms, coefs):
        total += c * (n // L)
    return total


def kth_good_index(k: int, nmax: int, lcms: list[int], coefs: list[int]) -> int:
    lo, hi = 1, nmax
    while lo < hi:
        mid = (lo + hi) // 2
        if count_good_indices_upto(mid, lcms, coefs) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def format_answer(index_n: int) -> str:
    last16 = fib_mod(index_n, LAST16_MOD)

    phi = (1.0 + 5.0 ** 0.5) / 2.0
    log10_f = index_n * math.log10(phi) - 0.5 * math.log10(5.0)

    exp = int(math.floor(log10_f))
    mant = 10.0 ** (log10_f - exp)
    mant = round(mant, 1)

    if mant >= 10.0:
        mant = 1.0
        exp += 1

    return f"{last16:016d},{mant:.1f}e{exp}"


def solve() -> str:
    mods = build_forbidden_moduli(NMAX)
    lcms, coefs = build_inclusion_exclusion(mods, NMAX)
    n = kth_good_index(TARGET, NMAX, lcms, coefs)
    return format_answer(n)


print(solve())