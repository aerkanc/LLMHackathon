from math import isqrt

LIMIT = 100_000_000

# Odd-only sieve up to LIMIT + 1
N = LIMIT + 1
SIZE = N // 2 + 1
sieve = bytearray(b"\x01") * SIZE
sieve[0] = 0

for p in range(3, isqrt(N) + 1, 2):
    if sieve[p >> 1]:
        start = (p * p) >> 1
        sieve[start::p] = b"\x00" * (((SIZE - start - 1) // p) + 1)

def is_prime(x: int) -> bool:
    return x == 2 or (x > 2 and (x & 1) and sieve[x >> 1])

# Small primes only for factorization
small_primes = [2] + [p for p in range(3, isqrt(LIMIT) + 1, 2) if sieve[p >> 1]]

total = 1  # n = 1 qualifies

# n + 1 must be prime, so iterate p = n + 1 over odd primes
for p in range(3, LIMIT + 2, 2):
    if not sieve[p >> 1]:
        continue

    n = p - 1

    # Necessary condition from divisor d = 2:
    # 2 + n/2 must be prime
    if not is_prime((n >> 1) + 2):
        continue

    # Factor n and reject if not squarefree
    temp = n
    factors = []
    squarefree = True

    for q in small_primes:
        if q * q > temp:
            break
        if temp % q == 0:
            temp //= q
            factors.append(q)
            if temp % q == 0:
                squarefree = False
                break

    if not squarefree:
        continue

    if temp > 1:
        factors.append(temp)

    # Generate all divisors from the distinct prime factors
    divisors = [1]
    for q in factors:
        divisors += [d * q for d in divisors]

    # Check d + n/d for all divisor pairs
    ok = True
    for d in divisors:
        if d <= n // d and not is_prime(d + n // d):
            ok = False
            break

    if ok:
        total += n

print(total)