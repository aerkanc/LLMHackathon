# Project Euler style – Problem 357: Prime generating integers
# Compute the sum of all n <= 10^8 such that for every divisor d of n, d + n/d is prime.

import numpy as np

LIMIT = 100_000_000

def sieve_bool(n: int) -> np.ndarray:
    """NumPy sieve: returns boolean array is_prime[0..n]."""
    is_prime = np.ones(n + 1, dtype=np.bool_)
    is_prime[:2] = False
    r = int(n**0.5)
    for p in range(2, r + 1):
        if is_prime[p]:
            is_prime[p*p:n+1:p] = False
    return is_prime

# We only ever need primality up to LIMIT+1 (since max d + n/d is n+1).
is_prime = sieve_bool(LIMIT + 1)

# Small primes up to sqrt(LIMIT) are enough for factoring n (<= 1e8).
PRIME_CAP = int(LIMIT**0.5) + 1
small_primes = [i for i in range(2, PRIME_CAP + 1) if is_prime[i]]

def factorize_squarefree(n: int):
    """
    Trial-divide n using small primes.
    Returns (ok, factors) where:
      ok = False if n has any squared prime factor (then n cannot be valid),
      factors = list of (p, exp) for remaining factorization (exp is 1 or leftover prime).
    """
    factors = []
    m = n
    for p in small_primes:
        if p * p > m:
            break
        if m % p == 0:
            cnt = 0
            while m % p == 0:
                m //= p
                cnt += 1
                if cnt > 1:
                    return False, []  # contains a square -> cannot be valid (2*d would be composite)
            factors.append((p, 1))
    if m > 1:
        factors.append((m, 1))  # leftover prime (power 1 due to squarefree check)
    return True, factors

def gen_divisors_from_factors(factors):
    """Generate all positive divisors from squarefree factor list."""
    divs = [1]
    for p, _ in factors:
        divs += [d * p for d in divs]
    return divs

# n must be even (since 1+n is prime) and not divisible by 4; equivalently n ≡ 2 (mod 4).
# Let p = n + 1 be prime and (p+3)//2 must also be prime (d = 2 check).
# Iterate over primes p ≡ 3 (mod 4) only, which ensures n ≡ 2 (mod 4).
primes = np.nonzero(is_prime)[0]
candidates = [int(p) for p in primes if (p <= LIMIT + 1 and (p & 3) == 3 and is_prime[(p + 3) >> 1])]

total_sum = 1  # n=1 is valid: divisors {1} -> 1+1=2 prime

for p in candidates:
    n = p - 1  # candidate n
    ok, factors = factorize_squarefree(n)
    if not ok:
        continue

    # Check the defining property for all divisors.
    good = True
    for d in gen_divisors_from_factors(factors):
        if not is_prime[d + n // d]:
            good = False
            break

    if good:
        total_sum += n

print(total_sum)
