from multiprocessing import Pool
import math
import os

# Precompute factorials for digits 0-9
factorial_cache = tuple(math.factorial(i) for i in range(10))

# Memoization cache for chain lengths (per-process)
chain_length_cache = {}


def digit_factorial_sum(n):
    """Calculate the sum of factorials of the digits of n"""
    total = 0
    while n > 0:
        digit = n % 10
        total += factorial_cache[digit]
        n //= 10
    return total


def get_chain_length(start):
    """
    Get the length of the chain before it repeats.
    Returns the count of unique numbers before entering a cycle.
    """
    if start in chain_length_cache:
        return chain_length_cache[start]

    seen = set()
    current = start

    # Keep applying the digit factorial operation until we see a repeated number
    while current not in seen:
        seen.add(current)
        current = digit_factorial_sum(current)

    length = len(seen)
    chain_length_cache[start] = length
    return length


def check_chain(start):
    """Return 1 if chain length is exactly 60, else 0"""
    return 1 if get_chain_length(start) == 60 else 0


if __name__ == '__main__':
    limit = 1000000
    target_length = 60

    # Use all available CPU cores
    num_workers = os.cpu_count() or 1

    # Parallelize the computation across all starting numbers
    with Pool(num_workers) as pool:
        results = pool.map(check_chain, range(1, limit), chunksize=10000)

    # Sum the results to get total count
    answer = sum(results)
    print(answer)