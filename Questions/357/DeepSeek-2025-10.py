import numpy as np
import multiprocessing as mp
from math import isqrt


def sieve(n):
    """Sieve of Eratosthenes to find all primes up to n"""
    is_prime = np.ones(n + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for i in range(2, isqrt(n) + 1):
        if is_prime[i]:
            is_prime[i * i:n + 1:i] = False
    return is_prime


def check_number(args):
    """Check if a number satisfies the prime-generating condition"""
    n, is_prime = args
    # Check all divisors d where d <= sqrt(n)
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            # Check both d + n/d and n/d + d (they're the same)
            if not is_prime[d + n // d]:
                return 0
    return n


def main():
    limit = 100000000
    print("Computing primes...")

    # We need primes up to limit + limit (for the case d=1, n/d could be up to limit)
    max_prime_needed = limit + limit // 2
    is_prime = sieve(max_prime_needed)

    print("Finding candidate numbers...")

    # Candidate numbers are n where n+1 is prime (from d=1 condition)
    candidates = []
    for p in range(2, limit + 2):
        if is_prime[p] and p - 1 <= limit:
            candidates.append(p - 1)

    print(f"Checking {len(candidates)} candidates...")

    # Use multiprocessing to check candidates in parallel
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.map(check_number, [(n, is_prime) for n in candidates])

    total_sum = sum(results)
    print(total_sum)


if __name__ == '__main__':
    main()