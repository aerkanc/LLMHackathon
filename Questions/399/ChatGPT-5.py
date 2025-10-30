# Squarefree Fibonacci Numbers – Project Euler style
# We need the 100,000,000th (N) squarefree Fibonacci number (by value of F(n)).
# Under the standard assumption used in the original problem statement:
# For every odd prime p != 5, the first n with p | F(n) is z(p) (rank of apparition),
# and p^2 | F(n) happens exactly when n is a multiple of p * z(p).
# For p = 2 and p = 5, we also get the same exclusion with m_p = 2*z(2)=6 and m_5=5*5=25.
#
# Hence an index n is "bad" (F(n) not squarefree) iff it is divisible by some m_p := p*z(p).
# We will:
#   1) Build all m_p with m_p <= X (X chosen large enough so that at least N good indices <= X).
#   2) Sieve [1..X] marking multiples of each m_p as bad using NumPy (memory ≈ X bytes).
#   3) Locate the Nth good index n_N.
#   4) Compute last 16 digits of F(n_N) by fast doubling mod 10^16.
#   5) Compute scientific notation ~ 10^{frac(n*log10(phi) - log10(sqrt(5)))} with 1 decimal.
#
# The sieve size X is chosen conservatively so we only do a single pass.

import numpy as np
import math
from math import log10

N = 100_000_000

# ----- helpers: fast doubling Fibonacci (mod m) -----
def fib_pair_mod(n, mod):
    if n == 0:
        return (0, 1)
    a, b = fib_pair_mod(n >> 1, mod)
    c = (a * ((b * 2 - a) % mod)) % mod
    d = (a * a + b * b) % mod
    if n & 1:
        return (d % mod, (c + d) % mod)
    else:
        return (c % mod, d % mod)

def fib_mod(n, mod):
    return fib_pair_mod(n, mod)[0] % mod

# Legendre symbol (5/p) for odd prime p (returns +1 or -1), special-case p=5
def legendre_5(p):
    if p == 5:
        return 0
    t = pow(5, (p - 1) // 2, p)
    return 1 if t == 1 else -1

# trial division primes up to limit
def primes_upto(m):
    sieve = bytearray(b"\x01") * (m + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(m**0.5) + 1):
        if sieve[i]:
            step = i
            start = i * i
            sieve[start:m+1:step] = b"\x00" * (((m - start) // step) + 1)
    return [i for i, v in enumerate(sieve) if v]

# factor small integer n (n <= ~2e4 here)
def factor_small(n, primes):
    fac = {}
    for p in primes:
        if p * p > n:
            break
        if n % p == 0:
            c = 0
            while n % p == 0:
                n //= p
                c += 1
            fac[p] = c
    if n > 1:
        fac[n] = 1
    return fac

# generate divisors from factorization dictionary
def gen_divisors(fac):
    divs = [1]
    for p, e in fac.items():
        cur = []
        pe = 1
        for _ in range(e + 1):
            for d in divs:
                cur.append(d * pe)
            pe *= p
        divs = cur
    return sorted(divs)

# rank of apparition z(p) for prime p (p != 5)
def rank_of_apparition(p, fib_mod_cache):
    if p == 5:
        return 5
    # z(p) | p - (5/p)
    d0 = p - legendre_5(p)
    # factor d0 and test divisors in increasing order
    # cache small primes for factoring
    if 'primes' not in rank_of_apparition.__dict__:
        rank_of_apparition.primes = primes_upto(20000)
    fac = factor_small(d0, rank_of_apparition.primes)
    for d in gen_divisors(fac):
        # F(d) ≡ 0 mod p ?
        if (p, d) in fib_mod_cache:
            fm = fib_mod_cache[(p, d)]
        else:
            fm = fib_mod(d, p)
            fib_mod_cache[(p, d)] = fm
        if fm == 0:
            return d
    # fallback (should not happen)
    return d0

# Choose a single large X so that #good >= N.
# Empirically density of good indices ~ 0.88..0.90; pick a safe headroom.
X = 130_000_000

# Build m_p list (p * z(p)) with m_p <= X
Pmax = int(X**0.5) + 200  # generous
plist = primes_upto(Pmax)
fib_mod_cache = {}

m_list = []

# p=2,5 special:
# z(2)=3 -> m=6 ; z(5)=5 -> m=25
if 6 <= X:
    m_list.append(6)
if 25 <= X:
    m_list.append(25)

for p in plist:
    if p in (2,5):
        continue
    z = rank_of_apparition(p, fib_mod_cache)
    m = p * z
    if m <= X:
        m_list.append(m)

m_list = sorted(set(m_list))

# Sieve bad indices (multiples of any m in m_list)
bad = np.zeros(X + 1, dtype=np.bool_)  # index 0 unused
for m in m_list:
    bad[m::m] = True

good = ~bad[1:]  # positions 1..X
good_count = int(good.sum())
if good_count < N:
    # If headroom wasn't enough (very unlikely with X above), extend X accordingly (single retry).
    # (Not expected to trigger.)
    raise SystemExit("Increase X; not enough good indices.")

# Find the Nth good index
# Using np.flatnonzero to get positions.
pos = np.flatnonzero(good)
nN = int(pos[N - 1] + 1)  # +1 because we started from index 1

# Compute last 16 digits of F(nN)
MOD = 10**16
last16 = fib_mod(nN, MOD)
last16_str = str(last16).zfill(16)

# Scientific notation of F(nN) using Binet's formula (float precision is sufficient for 1 decimal)
phi = (1 + 5**0.5) / 2.0
log10F = nN * log10(phi) - log10(5**0.5)
exp10 = int(math.floor(log10F))
frac = log10F - exp10
mant = 10 ** frac
mant_1dp = round(mant, 1)

# Handle rare 9.95.. rounding to 10.0 case
if mant_1dp >= 10.0:
    mant_1dp = 1.0
    exp10 += 1

print(f"{last16_str},{mant_1dp:.1f}e{exp10}")
