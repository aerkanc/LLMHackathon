from math import isqrt
from array import array

N = 10**8
limit = N // 2  # largest possible prime factor in a semiprime < N

# Odd-only sieve: index i represents number (2*i + 1)
size = limit // 2 + 1
sieve = bytearray(b"\x01") * size
sieve[0] = 0  # 1 is not prime

root = isqrt(limit)
for i in range(1, root // 2 + 1):
    if sieve[i]:
        p = 2 * i + 1
        start = (p * p) // 2
        sieve[start::p] = b"\x00" * (((size - 1 - start) // p) + 1)

primes = array('I', [2])
primes.extend(2 * i + 1 for i in range(1, size) if sieve[i])

count = 0
j = len(primes) - 1

for i, p in enumerate(primes):
    if p * p >= N:
        break
    while p * primes[j] >= N:
        j -= 1
    if j < i:
        break
    count += j - i + 1

print(count)