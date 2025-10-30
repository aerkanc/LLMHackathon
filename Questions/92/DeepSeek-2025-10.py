import numpy as np
from multiprocessing import Pool


def next_number(n):
    """Calculate the next number in the square digit chain"""
    total = 0
    while n > 0:
        digit = n % 10
        total += digit * digit
        n //= 10
    return total


def compute_chain_fate(start, limit=10000000):
    """Determine if starting number reaches 89 (returns True) or 1 (returns False)"""
    n = start
    while n != 1 and n != 89:
        n = next_number(n)
        # If we've already computed this number's fate in a previous run,
        # we could check a cache here, but for simplicity we'll just compute
    return n == 89


def process_chunk(args):
    """Process a chunk of numbers in parallel"""
    start, end = args
    count = 0
    for i in range(start, end):
        if compute_chain_fate(i):
            count += 1
    return count


def main():
    limit = 10000000

    # Use multiprocessing to utilize all 16 cores
    num_processes = 16
    chunk_size = limit // num_processes

    # Create ranges for each process
    chunks = []
    for i in range(num_processes):
        start = i * chunk_size + 1  # Start from 1
        end = (i + 1) * chunk_size if i < num_processes - 1 else limit
        chunks.append((start, end))

    # Process in parallel
    with Pool(processes=num_processes) as pool:
        results = pool.map(process_chunk, chunks)

    # Sum results from all processes
    total = sum(results)
    print(total)


if __name__ == '__main__':
    main()