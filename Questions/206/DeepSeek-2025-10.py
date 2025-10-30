import numpy as np
from multiprocessing import Pool
import math


def check_number(n):
    """Check if n^2 matches the pattern 1_2_3_4_5_6_7_8_9_0"""
    square = n * n
    s = str(square)

    # The square should have exactly 19 digits
    if len(s) != 19:
        return False

    # Check fixed positions in the pattern
    if (s[0] == '1' and s[2] == '2' and s[4] == '3' and
            s[6] == '4' and s[8] == '5' and s[10] == '6' and
            s[12] == '7' and s[14] == '8' and s[16] == '9' and
            s[18] == '0'):
        return True
    return False


def find_concealed_square_parallel():
    """Find the concealed square using parallel processing"""

    # Since the square ends with 0, the number must end with 0
    # Let's find the approximate range
    # The pattern is between 1020304050607080900 and 1929394959697989990
    min_sqrt = int(math.isqrt(1020304050607080900))
    max_sqrt = int(math.isqrt(1929394959697989990)) + 1

    # Since the square ends with 0, the number must end with 0
    # So we can step by 10
    start = (min_sqrt // 10) * 10
    end = max_sqrt

    # Create ranges for parallel processing
    num_processes = 16
    chunk_size = (end - start) // num_processes

    ranges = []
    for i in range(num_processes):
        chunk_start = start + i * chunk_size
        chunk_end = start + (i + 1) * chunk_size if i < num_processes - 1 else end
        ranges.append((chunk_start, chunk_end))

    def process_chunk(args):
        chunk_start, chunk_end = args
        # Only check numbers ending with 0 (since square ends with 0)
        for n in range(chunk_start, chunk_end, 10):
            if check_number(n):
                return n
        return None

    # Use multiprocessing to search in parallel
    with Pool(processes=num_processes) as pool:
        results = pool.map(process_chunk, ranges)

        # Find the first non-None result
        for result in results:
            if result is not None:
                return result

    return None


if __name__ == "__main__":
    result = find_concealed_square_parallel()
    print(result)