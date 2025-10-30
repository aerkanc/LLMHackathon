import math
from multiprocessing import Pool


def check_pattern(n):
    """Check if n² matches the pattern 1_2_3_4_5_6_7_8_9_0"""
    n_squared = n * n
    s = str(n_squared)

    if len(s) != 19:
        return None

    # Pattern positions (0-indexed):
    # Pos: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
    # Val: 1 ? 2 ? 3 ? 4 ? 5 ? 6  ?  7  ?  8  ?  9  ?  0
    expected_fixed = {
        0: '1', 2: '2', 4: '3', 6: '4', 8: '5',
        10: '6', 12: '7', 14: '8', 16: '9', 18: '0'
    }

    for pos, expected_digit in expected_fixed.items():
        if s[pos] != expected_digit:
            return None

    return n


def search_range(args):
    """Search a range of multiples of 10"""
    start, end = args
    for n in range(start, end, 10):
        result = check_pattern(n)
        if result is not None:
            return result
    return None


if __name__ == '__main__':
    # Set up the search range
    min_n = 10 ** 9  # sqrt(10^18)
    max_n = int(math.sqrt(10 ** 19)) + 1

    # Align to multiples of 10
    if min_n % 10 != 0:
        min_n = ((min_n // 10) + 1) * 10

    # Create ranges for parallel processing
    num_workers = 16
    total_numbers = (max_n - min_n) // 10
    chunk_size = max(1, (total_numbers // num_workers) * 10)

    ranges = []
    for i in range(num_workers):
        start = min_n + i * chunk_size
        end = min_n + (i + 1) * chunk_size if i < num_workers - 1 else max_n
        if start < max_n:
            ranges.append((start, end))

    # Parallel search
    with Pool(num_workers) as pool:
        results = pool.map(search_range, ranges)

    # Find and print the result
    for result in results:
        if result is not None:
            print(result)
            break