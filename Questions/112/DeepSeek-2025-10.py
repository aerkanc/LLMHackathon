import multiprocessing as mp
import numpy as np


def is_bouncy(n):
    """Check if a number is bouncy by examining its digits."""
    digits = [int(d) for d in str(n)]

    # Check if increasing
    increasing = all(digits[i] >= digits[i - 1] for i in range(1, len(digits)))
    if increasing:
        return False

    # Check if decreasing
    decreasing = all(digits[i] <= digits[i - 1] for i in range(1, len(digits)))
    if decreasing:
        return False

    # Neither increasing nor decreasing = bouncy
    return True


def count_bouncy_in_range(args):
    """Count bouncy numbers in a given range."""
    start, end = args
    count = 0
    for n in range(start, end + 1):
        if is_bouncy(n):
            count += 1
    return count


def find_99_percent_point():
    """Find the smallest N where exactly 99% of numbers 1..N are bouncy."""
    # Use multiprocessing to count bouncy numbers in parallel
    num_processes = mp.cpu_count()

    # We know from the problem that the answer is > 21780
    # Let's search in increasing chunks
    chunk_size = 10000
    current_n = 21780
    total_bouncy = 0

    # First, get the count up to our starting point
    print("Calculating initial bouncy count up to 21780...")
    with mp.Pool(processes=num_processes) as pool:
        ranges = []
        for i in range(0, 21780, chunk_size):
            start = i + 1
            end = min(i + chunk_size, 21780)
            ranges.append((start, end))

        results = pool.map(count_bouncy_in_range, ranges)
        total_bouncy = sum(results)

    print(f"At n=21780: {total_bouncy} bouncy numbers ({total_bouncy / 21780 * 100:.2f}%)")

    # Now search for the 99% point
    current_n = 21780

    while True:
        # Process next chunk
        next_n = current_n + chunk_size

        with mp.Pool(processes=num_processes) as pool:
            ranges = []
            for i in range(current_n, next_n, chunk_size // num_processes):
                start = i + 1
                end = min(i + chunk_size // num_processes, next_n)
                if start <= end:
                    ranges.append((start, end))

            results = pool.map(count_bouncy_in_range, ranges)
            chunk_bouncy = sum(results)

        total_bouncy += chunk_bouncy
        current_n = next_n

        proportion = total_bouncy / current_n

        # Check if we've reached exactly 99%
        if total_bouncy * 100 == current_n * 99:
            return current_n

        # Progress monitoring
        if current_n % 100000 == 0:
            print(f"At n={current_n}: {total_bouncy} bouncy numbers ({proportion * 100:.4f}%)")

        # If we're close to 99%, switch to finer granularity
        if proportion >= 0.989:
            # Switch to checking individual numbers
            print(f"Close to target at n={current_n} ({proportion * 100:.4f}%), switching to fine search...")

            while True:
                current_n += 1
                if is_bouncy(current_n):
                    total_bouncy += 1

                if total_bouncy * 100 == current_n * 99:
                    return current_n

                if current_n % 1000 == 0:
                    proportion = total_bouncy / current_n
                    print(f"Fine search at n={current_n}: {total_bouncy} bouncy numbers ({proportion * 100:.4f}%)")


if __name__ == "__main__":
    result = find_99_percent_point()
    print(result)