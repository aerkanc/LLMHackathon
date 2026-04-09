import numpy as np
import multiprocessing as mp

# Problem parameters
LIMIT = 100_000_000

# Allocate sieve globally to take advantage of Copy-On-Write sharing across processes in Linux
sieve = np.ones(LIMIT + 2, dtype=np.bool_)

def init_sieve():
    """Generates prime numbers up to LIMIT + 1 using a fast Numpy sieve."""
    sieve[0:2] = False
    for i in range(2, int((LIMIT + 1)**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = False

def check(n):
    """
    Checks if for all divisors d of n (from 3 to sqrt(n)), d + n/d is prime.
    d=1 and d=2 are inherently guaranteed to be prime based on the pre-filtering logic.
    """
    for d in range(3, int(n**0.5) + 1):
        if n % d == 0:
            if not sieve[d + n // d]:
                return 0
    return n

def main():
    init_sieve()

    # If n is a prime generating integer, 1 + n/1 = n + 1 must be prime.
    # Therefore, n = p - 1 for some prime p.
    primes = np.nonzero(sieve)[0]
    candidates = primes - 1
    candidates = candidates[candidates <= LIMIT]

    # Furthermore, all valid n > 1 must be even.
    # Therefore, 2 is a divisor. So 2 + n/2 must be prime.
    # (Note: for n=1, 1//2 + 2 = 2 which is prime, safely keeping 1 as a candidate).
    idx = sieve[candidates // 2 + 2]
    candidates = candidates[idx]

    # An integer generating primes this way must be square-free.
    # Pre-filtering common prime squares significantly reduces the workload.
    candidates = candidates[candidates % 4 != 0]
    candidates = candidates[candidates % 9 != 0]
    candidates = candidates[candidates % 25 != 0]
    candidates = candidates[candidates % 49 != 0]
    candidates = candidates[candidates % 121 != 0]

    # Distribute the remaining resilient candidates across the available 16 cores
    with mp.Pool() as pool:
        # A chunksize of 2000 is balanced to minimize IPC overhead
        results = pool.map(check, candidates, chunksize=2000)

    # Print only the final computed sum
    print(sum(results))

if __name__ == '__main__':
    main()