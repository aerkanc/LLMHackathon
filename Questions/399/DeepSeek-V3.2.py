import numpy as np
import math
from decimal import Decimal, getcontext, ROUND_HALF_UP

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------
def sieve(limit: int):
    """Return list of primes up to limit."""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            step = i
            start = i * i
            is_prime[start:limit+1:step] = [False] * ((limit - start) // step + 1)
    return [i for i, v in enumerate(is_prime) if v]

def compute_z(p: int) -> int:
    """Return the rank of apparition z(p) for prime p (Wall's conjecture)."""
    if p == 5:
        return 5
    # upper bound for z(p)
    if p % 5 in (1, 4):
        m = p - 1
    else:
        m = 2 * (p + 1)
    a, b = 1, 1          # F1, F2
    for n in range(3, m + 1):
        a, b = b, (a + b) % p
        if b == 0:
            return n
    # Should never happen
    return None

def fib_mod(n: int, mod: int):
    """Return (F_n % mod, F_{n+1} % mod) using fast doubling."""
    a, b = 0, 1          # F0, F1
    bits = n.bit_length()
    for i in range(bits - 1, -1, -1):
        c = (a * ((2 * b - a) % mod)) % mod
        d = (a * a + b * b) % mod
        if (n >> i) & 1:
            a, b = d, (c + d) % mod
        else:
            a, b = c, d
    return a, b

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    TARGET = 100_000_000
    U = 200_000_000                 # safe upper bound for the index
    MAX_PRIME = 25000               # primes up to 25000 are enough

    # ---- 1. Build list of all d = p * z(p) that are <= U ----
    primes = sieve(MAX_PRIME)
    divisors = []
    for p in primes:
        z = compute_z(p)
        d = p * z
        if d <= U:
            divisors.append(d)

    # ---- 2. Sieve: mark all multiples of these d as "bad" ----
    bad = np.zeros(U + 1, dtype=np.uint8)
    bad[0] = 1                     # index 0 is not used
    for d in divisors:
        bad[d::d] = 1

    # ---- 3. Find the TARGET‑th good index ----
    good_indices = np.flatnonzero(bad == 0)   # all indices i with bad[i]==0
    n0 = good_indices[TARGET - 1]             # the required index

    # free memory
    del bad, good_indices

    # ---- 4. Last 16 digits of F_n0 ----
    MOD = 10 ** 16
    last16 = fib_mod(n0, MOD)[0]

    # ---- 5. Scientific notation (rounded to one decimal) ----
    getcontext().prec = 50
    sqrt5 = Decimal(5).sqrt()
    phi = (Decimal(1) + sqrt5) / 2
    log10_phi = phi.log10()
    log10_sqrt5 = sqrt5.log10()
    f = Decimal(n0) * log10_phi - log10_sqrt5
    exp = int(f)                     # floor(log10(F_n0))
    mantissa = Decimal(10) ** (f - exp)
    # round to one decimal place, half up
    rounded = mantissa.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
    if rounded >= 10:
        rounded = Decimal('1.0')
        exp += 1
    scientific = f"{rounded:.1f}e{exp}"

    # ---- 6. Output ----
    print(f"{last16:016d},{scientific}")

if __name__ == "__main__":
    main()