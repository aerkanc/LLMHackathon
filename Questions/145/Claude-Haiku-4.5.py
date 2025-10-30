from multiprocessing import Pool


def all_digits_odd(n):
    """Check if all digits of n are odd (1, 3, 5, 7, 9)"""
    while n > 0:
        digit = n % 10
        if digit % 2 == 0:  # Even digit found
            return False
        n //= 10
    return True


def reverse_number(n):
    """Reverse the digits of n"""
    rev = 0
    while n > 0:
        rev = rev * 10 + n % 10
        n //= 10
    return rev


def count_reversible_range(start, end):
    """Count reversible numbers in the range [start, end)"""
    count = 0
    for n in range(start, end):
        # Skip if n ends with 0 (reverse would have leading zeros)
        if n % 10 == 0:
            continue

        # Reverse n and compute sum
        rev_n = reverse_number(n)
        s = n + rev_n

        # Check if all digits of the sum are odd
        if all_digits_odd(s):
            count += 1

    return count


if __name__ == '__main__':
    limit = 1000000000  # 10^9
    num_processes = 16
    chunk_size = limit // num_processes

    # Create ranges for each process
    ranges = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_processes)]

    # Use multiprocessing pool to parallelize
    with Pool(num_processes) as pool:
        results = pool.starmap(count_reversible_range, ranges)

    # Sum results from all processes
    total = sum(results)
    print(total)