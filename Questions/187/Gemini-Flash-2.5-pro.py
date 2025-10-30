import numpy as np


def solve_problem_187():
    """
    Computes the number of composite integers n < 10^8
    that have precisely two, not necessarily distinct, prime factors.
    """

    # Set the limit N
    N = 100_000_000

    # We need to find primes p and q such that p <= q and p * q < N.
    # The smallest p can be is 2. The largest q can be is < N / 2.
    # So, we need to sieve for primes up to N // 2.
    sieve_limit = N // 2

    # Use numpy for an efficient boolean sieve
    try:
        sieve = np.ones(sieve_limit + 1, dtype=bool)
    except MemoryError:
        # This should not happen with 64GB of RAM, but as a safeguard.
        return

    # 0 and 1 are not prime
    sieve[0:2] = False

    # Perform the Sieve of Eratosthenes
    # We only need to check up to sqrt(sieve_limit)
    for i in range(2, int(sieve_limit ** 0.5) + 1):
        if sieve[i]:
            # Mark all multiples of i as not prime
            # Start from i*i, as smaller multiples are already covered
            sieve[i * i:: i] = False

    # Extract the prime numbers from the sieve
    primes = np.flatnonzero(sieve)

    count = 0
    num_primes = len(primes)

    # Iterate through all possible primes p
    for i in range(num_primes):
        p = primes[i]

        # Optimization: If p*p >= N, then p*q (with q >= p) must also be >= N.
        # We can stop the entire search.
        # Use p * p to avoid floating point operations of sqrt
        if p * p >= N:
            break

        # Iterate through all possible primes q, starting from p (j=i)
        # to satisfy the p <= q condition.
        for j in range(i, num_primes):
            q = primes[j]

            # Check if the product is within the limit
            if p * q >= N:
                # Since the primes list is sorted, any further q
                # in this inner loop will also exceed the limit.
                break

            # If p * q < N, we found a valid composite number
            count += 1

    # Print only the final answer
    print(count)


if __name__ == "__main__":
    solve_problem_187()
