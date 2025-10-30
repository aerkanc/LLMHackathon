import numpy
import multiprocessing
import os
import time

# The upper limit for n
N_LIMIT = 100_000_000

# Global variable to hold the prime sieve for worker processes
g_primes = None


def init_worker(primes_array):
    """
    Initializer for the multiprocessing pool.
    Sets the global 'g_primes' variable for each worker process.
    This uses copy-on-write memory, which is very efficient.
    """
    global g_primes
    g_primes = primes_array


def check_n(n):
    """
    Checks if a single number 'n' satisfies the Project Euler 357 conditions.

    It assumes:
    1. n+1 is prime (which is how 'n' is generated).
    2. The 'g_primes' array is available globally.

    It checks:
    1. If 'n' is square-free.
    2. If d + n/d is prime for all divisors d.

    Returns 'n' if valid, and 0 if invalid.
    """
    global g_primes

    # We only need to check divisors up to the square root of n.
    limit = int(n ** 0.5)

    # We start from d=2 because d=1 is (1 + n/1) = n+1, which is guaranteed
    # to be prime by our candidate generation.
    for d in range(2, limit + 1):
        if n % d == 0:
            # We found a divisor 'd'. 'n/d' is its pair.

            # Check 1: Is 'n' square-free?
            # If n is not square-free, it has a prime factor p such that p^2 | n.
            # Since p^2 <= n, we know p <= sqrt(n).
            # The loop will eventually hit d=p. At that point, n % (p*p) == 0.
            # This check is sufficient to prove 'n' is not square-free.
            if n % (d * d) == 0:
                return 0  # Not square-free

            # Check 2: Is d + n/d prime?
            # We look up the pre-computed sum in our sieve.
            if not g_primes[d + n // d]:
                return 0  # Fails the prime sum condition

    # If the loop completes without returning 0, 'n' is a valid solution.
    return n


def solve():
    """
    Main solver function.
    Calculates the sieve, sets up the parallel pool, sums the results,
    and prints the final answer.
    """
    N = N_LIMIT

    # --- Step 1: Create Prime Sieve ---
    # We need to check primality for n+1 (up to N+1) and
    # for d + n/d (also up to N+1, for d=1).
    # A sieve up to N+2 is required.
    try:
        primes = numpy.ones(N + 2, dtype=numpy.bool_)
        primes[0:2] = False  # 0 and 1 are not prime

        # Sieve of Eratosthenes
        for i in range(2, int((N + 2) ** 0.5) + 1):
            if primes[i]:
                # Mark all multiples of i as not prime
                primes[i * i::i] = False
    except MemoryError:
        # This shouldn't happen with 64GB RAM, but good to be safe
        print("Error: Not enough memory to create the prime sieve.")
        return

    # --- Step 2: Get Candidate 'n' Values ---
    # Our candidates are n = p - 1, where p is a prime.
    # We handle n=1 separately.
    # `numpy.flatnonzero` is a fast way to get the indices where `primes` is True.
    # We start from index 3 (prime '3'), so n = 3 - 1 = 2.
    candidate_primes_p = numpy.flatnonzero(primes[3:]) + 3

    # Use numpy's vectorized subtraction for speed
    candidate_n_values = candidate_primes_p - 1

    # --- Step 3: Run Checks in Parallel ---

    # Start sum with 1 (for the n=1 solution, where 1+1/1=2 is prime)
    total_sum = 1

    # Determine the number of cores to use (as per hackathon spec)
    try:
        # Use os.sched_getaffinity(0) on Linux for accurate core count
        num_cores = len(os.sched_getaffinity(0))
    except AttributeError:
        # Fallback for other OSes
        num_cores = os.cpu_count() or 1

    # Limit to 16 cores as specified
    num_cores = min(num_cores, 16)

    # Use 'with' statement for proper pool management
    with multiprocessing.Pool(processes=num_cores,
                              initializer=init_worker,
                              initargs=(primes,)) as pool:

        # Calculate a good chunksize for efficient work distribution
        # Divide total work into many small chunks
        chunksize = max(1, len(candidate_n_values) // (num_cores * 4))

        # 'imap_unordered' is generally the fastest way to map and reduce
        # It doesn't preserve order, which we don't need.
        results = pool.imap_unordered(check_n, candidate_n_values, chunksize=chunksize)

        # 'check_n' returns either 0 (invalid) or 'n' (valid)
        # We can sum these results directly.
        for valid_n in results:
            total_sum += valid_n

    # --- Step 4: Print the Final Answer ---
    # The ONLY output of the script must be the final answer.
    print(total_sum)


if __name__ == "__main__":
    solve()
