import numpy as np
import math

N = 100_000_000

# Sieve of Eratosthenes up to N+1
isprime = np.ones(N + 2, dtype=np.bool_)
isprime[0] = isprime[1] = False
for i in range(2, int(math.isqrt(N + 1)) + 1):
    if isprime[i]:
        isprime[i*i::i] = False

# good[n] = True if n passes all divisor-pair checks
good = np.zeros(N + 1, dtype=np.bool_)
good[1] = True  # n=1: 1+1=2 is prime

# For n>1: n must be ≡ 2 (mod 4), n+1 prime, n/2+2 prime
idx = np.arange(2, N + 1, 4, dtype=np.int32)  # 2, 6, 10, 14, ...
mask = isprime[idx + 1] & isprime[idx // 2 + 2]
good[idx[mask]] = True

# Sieve: for each d >= 3, for each e >= d with d*e <= N,
# if d+e is not prime, mark d*e as bad.
# Skip d ≡ 0 mod 4 (those n are already excluded).
# For odd d: only e ≡ 2 mod 4 gives n ≡ 2 mod 4.
# For d ≡ 2 mod 4: only odd e gives n ≡ 2 mod 4.

max_d = int(math.isqrt(N))

for d in range(3, max_d + 1):
    max_e = N // d
    if max_e < d:
        break

    if d % 4 == 0:
        continue

    if d % 2 == 1:  # odd d, need e ≡ 2 mod 4
        r = d % 4
        if r == 1:
            start = d + 1  # d+1 ≡ 2 mod 4
        else:  # r == 3
            start = d + 3  # d+3 ≡ 2 mod 4
            if start < d:
                start += 4
        if start > max_e:
            continue
        e = np.arange(start, max_e + 1, 4, dtype=np.int32)
    else:  # d ≡ 2 mod 4, need odd e
        start = d + 1  # first odd >= d (d is even)
        if start > max_e:
            continue
        e = np.arange(start, max_e + 1, 2, dtype=np.int32)

    n_vals = d * e
    bad = ~isprime[d + e]
    if np.any(bad):
        good[n_vals[bad]] = False

# Sum all good n
result = np.sum(np.nonzero(good)[0].astype(np.int64))
print(result)