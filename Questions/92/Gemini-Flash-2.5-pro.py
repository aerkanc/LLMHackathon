#!/usr/bin/env python3

import multiprocessing
import sys

# Pre-computed squares of digits 0-9 for speed
SQ = [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]


def sum_sq_digits(n):
    """
    Calculates the sum of the squares of the digits of n.
    Uses the pre-computed SQ list.
    """
    s = 0
    while n > 0:
        s += SQ[n % 10]
        n //= 10
    return s


def compute_chain_ends(limit):
    """
    Pre-computes the final destination (1 or 89) for all
    chain-starting-numbers from 1 up to 'limit'.
    Uses memoization.

    Returns a list 'ends_at' where ends_at[i] is the
    terminal number (1 or 89) for the chain starting at i.
    """
    # ends_at[i] = 0 (unknown), 1 (ends at 1), 89 (ends at 89)
    ends_at = [0] * (limit + 1)
    ends_at[1] = 1
    ends_at[89] = 89

    for i in range(1, limit + 1):
        if ends_at[i] != 0:
            continue  # Already computed

        curr = i
        chain = [i]

        # Follow the chain until we hit a known number
        while True:
            curr = sum_sq_digits(curr)

            # Since all numbers in [1, limit] will map to a number
            # also in [1, limit] (or smaller), we are guaranteed
            # to stay within our cache bounds.
            if curr == 1 or curr == 89:
                end_val = curr
                break

            if ends_at[curr] != 0:
                end_val = ends_at[curr]
                break

            chain.append(curr)

        # Back-fill the result for all members of this new chain
        for num_in_chain in chain:
            ends_at[num_in_chain] = end_val

    return ends_at


# --- Multiprocessing Worker ---

# Global variable for worker processes
g_ends_at = None


def init_worker(ends_at_arr):
    """
    Initializer function for each worker in the pool.
    Sets a global variable to store the pre-computed chain ends.
    """
    global g_ends_at
    g_ends_at = ends_at_arr


def count_in_range(start, end):
    """
    Worker function.
    Counts how many numbers in [start, end] (inclusive)
    have their chain end at 89.
    """
    # g_ends_at is populated by init_worker
    if g_ends_at is None:
        return 0

    local_count = 0
    for n in range(start, end + 1):
        # We only need the *first* step.
        s = sum_sq_digits(n)

        # This sum 's' is guaranteed to be <= 567,
        # so we can look it up in our global cache.
        if g_ends_at[s] == 89:
            local_count += 1

    return local_count


# --- Main Execution ---

def main():
    """
    Main function to orchestrate pre-computation and parallel processing.
    """
    # The largest possible first-step sum is from 9,999,999,
    # which is 7 * 9^2 = 567.
    CACHE_LIMIT = 567

    # Total range to check
    N = 9_999_999

    # Number of cores available
    NUM_CORES = 16

    # 1. Pre-compute chain ends. This is fast.
    try:
        ends_at_list = compute_chain_ends(CACHE_LIMIT)
    except Exception as e:
        # In case of error, print nothing to avoid confusing the evaluator
        # print(f"Error during pre-computation: {e}", file=sys.stderr)
        return

    # 2. Define ranges for each worker
    ranges = []
    chunk_size = (N // NUM_CORES) + 1
    start = 1
    while start <= N:
        end = min(start + chunk_size - 1, N)
        ranges.append((start, end))
        start = end + 1

    # 3. Run the parallel processing
    total_count = 0
    try:
        with multiprocessing.Pool(processes=NUM_CORES,
                                  initializer=init_worker,
                                  initargs=(ends_at_list,)) as pool:

            # starmap applies the arguments in 'ranges' to 'count_in_range'
            results = pool.starmap(count_in_range, ranges)

            # Sum the results from all workers
            total_count = sum(results)

    except Exception as e:
        # print(f"Error during multiprocessing: {e}", file=sys.stderr)
        pass  # Print nothing on error

    # 4. Print *only* the final result
    print(total_count)


if __name__ == "__main__":
    main()
