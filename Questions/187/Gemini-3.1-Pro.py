import numpy as np
import bisect


def solve():
    limit = 10 ** 8 - 1
    max_prime = limit // 2

    # Sieve of Eratosthenes using numpy for fast vectorization
    # We only store odd numbers to halve the memory and processing time
    s = np.ones(max_prime // 2 + 1, dtype=bool)
    s[0] = False  # 1 is not a prime

    for i in range(3, int(max_prime ** 0.5) + 1, 2):
        if s[i // 2]:
            s[(i * i) // 2:: i] = False

    # Combine the only even prime (2) with the sieved odd primes
    primes = np.r_[2, 2 * np.nonzero(s)[0] + 1]

    # Ensure no primes exceed max_prime due to array dimension rounding
    primes = primes[primes <= max_prime]

    count = 0

    # Count valid semiprime pairs (p * q < 10**8 where p <= q)
    for i, p in enumerate(primes):
        if p * p > limit:
            break

        # We need the number of primes q >= p such that q <= limit // p
        # bisect_right returns the index representing the count of primes <= limit // p
        idx = bisect.bisect_right(primes, limit // p)

        # Valid pairs using current `p` is (idx - i) since we only want q >= p
        count += (idx - i)

    print(count)


if __name__ == '__main__':
    solve()