import math
import numpy as np
from multiprocessing import Pool


def sieve(n):
    """Generate primes up to n using sieve of Eratosthenes"""
    if n < 2:
        return []
    sieve = np.ones(n + 1, dtype=bool)
    sieve[0] = sieve[1] = False
    sieve[2 * 2:n + 1:2] = False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if sieve[i]:
            sieve[i * i:n + 1:i] = False
    return np.where(sieve)[0]


def count_for_prime(args):
    """Count valid pairs for a given prime p"""
    p, primes = args
    max_q = 10 ** 8 // p
    # Count primes q where p <= q <= max_q
    # Find the first index where primes >= p
    start_idx = np.searchsorted(primes, p)
    # Find the last index where primes <= max_q
    end_idx = np.searchsorted(primes, max_q, side='right') - 1
    if end_idx >= start_idx:
        return end_idx - start_idx + 1
    return 0


def main():
    limit = 10 ** 8
    sqrt_limit = int(math.sqrt(limit))

    # Generate all primes up to limit/2 (since smaller prime can be 2)
    print("Generating primes...")
    primes = sieve(limit // 2)
    print(f"Generated {len(primes)} primes")

    # Get small primes (p ≤ √limit)
    small_primes = primes[primes <= sqrt_limit]
    print(f"Processing {len(small_primes)} small primes")

    # Parallelize the counting
    with Pool() as pool:
        args = [(p, primes) for p in small_primes]
        counts = pool.map(count_for_prime, args)

    result = sum(counts)
    print(result)


if __name__ == "__main__":
    main()