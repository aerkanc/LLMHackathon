import math
import numpy as np
from multiprocessing import Pool


def sieve(n):
    """Generate primes up to n using Sieve of Eratosthenes"""
    if n < 2:
        return []
    sieve = np.ones(n + 1, dtype=bool)
    sieve[0] = sieve[1] = False
    sieve[2 * 2::2] = False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if sieve[i]:
            sieve[i * i::2 * i] = False
    primes = np.where(sieve)[0].astype(np.int32)
    return primes


def compute_M(args):
    """Compute M(p,q,N) for a given prime pair"""
    p, q, N = args
    if p * q > N:
        return 0

    max_val = 0
    p_power = p
    while p_power <= N:
        q_power = q
        while p_power * q_power <= N:
            max_val = max(max_val, p_power * q_power)
            q_power *= q
        p_power *= p

    return max_val


def S(N):
    """Compute S(N) - sum of all distinct M(p,q,N)"""
    primes = sieve(N)
    prime_list = primes.tolist()

    # Generate all prime pairs (p,q) where p < q and p*q <= N
    pairs = []
    for i in range(len(prime_list)):
        p = prime_list[i]
        if p * p > N:  # No need to check larger primes
            break
        for j in range(i + 1, len(prime_list)):
            q = prime_list[j]
            if p * q > N:
                break
            pairs.append((p, q, N))

    # Use multiprocessing to compute M values in parallel
    with Pool() as pool:
        results = pool.map(compute_M, pairs)

    # Sum distinct M values (0 values are excluded as they don't contribute)
    distinct_M = set(results)
    return sum(distinct_M)


if __name__ == "__main__":
    result = S(100000000)
    print(result)