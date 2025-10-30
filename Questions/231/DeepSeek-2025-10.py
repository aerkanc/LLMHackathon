import math
import numpy as np
from multiprocessing import Pool, cpu_count


def sieve(n):
    """Sieve of Eratosthenes to find all primes up to n"""
    if n < 2:
        return []

    sieve = np.ones(n + 1, dtype=bool)
    sieve[0] = sieve[1] = False

    for i in range(2, int(math.sqrt(n)) + 1):
        if sieve[i]:
            sieve[i * i:n + 1:i] = False

    primes = np.where(sieve)[0].astype(np.int64)
    return primes


def prime_exponent_in_factorial(n, p):
    """Calculate exponent of prime p in n! using Legendre's formula"""
    exponent = 0
    power = p
    while power <= n:
        exponent += n // power
        power *= p
    return exponent


def process_prime_chunk(args):
    """Process a chunk of primes and return their contribution to the sum"""
    primes_chunk, n, k, n_minus_k = args
    total = 0
    for p in primes_chunk:
        exponent = (prime_exponent_in_factorial(n, p) -
                    prime_exponent_in_factorial(k, p) -
                    prime_exponent_in_factorial(n_minus_k, p))
        total += p * exponent
    return total


def main():
    n = 20000000
    k = 15000000
    n_minus_k = n - k

    # Generate all primes up to n
    primes = sieve(n)

    # Split primes into chunks for parallel processing
    num_workers = min(cpu_count(), 16)  # Use up to 16 cores
    chunk_size = (len(primes) + num_workers - 1) // num_workers

    # Prepare arguments for each worker
    chunks = []
    for i in range(num_workers):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, len(primes))
        if start < end:
            chunks.append((primes[start:end], n, k, n_minus_k))

    # Process in parallel
    with Pool(processes=num_workers) as pool:
        results = pool.map(process_prime_chunk, chunks)

    # Sum all contributions
    total_sum = sum(results)
    print(total_sum)


if __name__ == "__main__":
    main()