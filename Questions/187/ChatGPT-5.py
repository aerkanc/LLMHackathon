# Project Euler–style Problem 187: Count semiprimes < 10^8
# Uses a fast odd-only NumPy sieve and a two-pointer count of prime pairs (p <= q, p*q < LIMIT)

import numpy as np

LIMIT = 10**8

# Sieve only odd numbers: index i represents number 2*i + 1
size = LIMIT // 2
sieve = np.ones(size, dtype=bool)
sieve[0] = False  # 1 is not prime

root = int(LIMIT**0.5)
for p in range(3, root + 1, 2):
    if sieve[p // 2]:
        start = (p * p) // 2
        sieve[start::p] = False  # strike multiples of p among odds

# Build prime array (include 2)
odd_primes = 2 * np.nonzero(sieve)[0] + 1
primes = np.concatenate((np.array([2], dtype=np.int64), odd_primes.astype(np.int64)))

# Two-pointer count of semiprimes n = p*q with p <= q and p*q < LIMIT
i, j = 0, len(primes) - 1
count = 0

while i <= j:
    p = int(primes[i])
    # Move j left until p * primes[j] < LIMIT
    while i <= j and p * int(primes[j]) >= LIMIT:
        j -= 1
    if i > j:
        break
    count += (j - i + 1)
    i += 1

print(count)
