import numpy as np
from multiprocessing import Pool


def precompute_factorials():
    """Precompute factorials for digits 0-9"""
    fact = np.ones(10, dtype=np.int64)
    for i in range(2, 10):
        fact[i] = fact[i - 1] * i
    return fact


def digit_factorial_sum(n, fact):
    """Calculate sum of factorials of digits of n"""
    total = 0
    while n > 0:
        total += fact[n % 10]
        n //= 10
    return total


def process_chunk(args):
    """Process a chunk of numbers to count chains of length 60"""
    start, end, fact = args
    count = 0

    # Local memoization for this chunk
    chain_lengths = {}

    for n in range(start, end):
        seen = {}
        current = n
        pos = 0

        while current not in seen:
            if current in chain_lengths:
                # We've computed this chain before
                total_length = pos + chain_lengths[current]
                chain_lengths[n] = total_length
                if total_length == 60:
                    count += 1
                break

            seen[current] = pos
            current = digit_factorial_sum(current, fact)
            pos += 1
        else:
            # Found a cycle
            cycle_start_pos = seen[current]
            chain_len = pos - cycle_start_pos

            # Update chain lengths for all numbers in this chain
            for num, position in seen.items():
                if position >= cycle_start_pos:
                    chain_lengths[num] = chain_len
                else:
                    chain_lengths[num] = pos - position

            if pos == 60:  # Non-repeating chain length is exactly 60
                count += 1

    return count


def main():
    fact = precompute_factorials()
    limit = 1000000

    # Use multiprocessing to parallelize the computation
    num_processes = 16
    chunk_size = limit // num_processes

    chunks = []
    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_processes - 1 else limit
        chunks.append((start, end, fact))

    with Pool(processes=num_processes) as pool:
        results = pool.map(process_chunk, chunks)

    total = sum(results)
    print(total)


if __name__ == "__main__":
    main()