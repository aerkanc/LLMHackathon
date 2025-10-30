import multiprocessing
import os


def count_reversible_in_range(start, end):
    """
    Counts the number of reversible numbers in a given range [start, end).
    This function is designed to be run in a separate process.
    """
    count = 0
    # Ensure start is at least 1
    if start == 0:
        start = 1

    for n in range(start, end):
        # Optimization 1: Skip numbers ending in 0
        if n % 10 == 0:
            continue

        # Reverse the number n
        rev = 0
        temp = n
        while temp > 0:
            rev = rev * 10 + temp % 10
            temp //= 10

        # Optimization 2: Only check n if n < rev(n)
        # This avoids double-counting and skips palindromes.
        if n < rev:
            s = n + rev
            all_odd = True

            # Check if all digits of the sum are odd
            if s == 0:  # Should not be hit, but good practice
                all_odd = False
            else:
                while s > 0:
                    if (s % 10) % 2 == 0:
                        all_odd = False
                        break
                    s //= 10

            if all_odd:
                # If n is reversible, rev(n) is also reversible.
                # Since n < rev, and rev(n) will be in a similar magnitude
                # (same number of digits), we can be sure rev(n) < 10^9.
                count += 2

    return count


def solve_problem():
    """
    Solves the problem by splitting the range among multiple cores.
    """
    LIMIT = 1_000_000_000
    # Use 16 cores as specified in the problem
    NUM_CORES = 16

    step = LIMIT // NUM_CORES
    ranges = []
    for i in range(NUM_CORES):
        start = i * step
        end = (i + 1) * step
        ranges.append((start, end))

    # Adjust the last range to cover up to LIMIT exactly
    ranges[-1] = (ranges[-1][0], LIMIT)

    total_count = 0
    try:
        # Use a context manager for the pool
        with multiprocessing.Pool(processes=NUM_CORES) as pool:
            # Use starmap to pass (start, end) arguments to the worker
            results = pool.starmap(count_reversible_in_range, ranges)

        # Sum the results from all processes
        total_count = sum(results)

    except Exception as e:
        # In a real-world scenario, you might log errors.
        # For this problem, we'll just print 0 if it fails.
        total_count = 0
        # print(f"An error occurred: {e}", file=sys.stderr) # Avoid debug output

    # The final answer is printed to stdout
    print(total_count)


if __name__ == "__main__":
    solve_problem()
