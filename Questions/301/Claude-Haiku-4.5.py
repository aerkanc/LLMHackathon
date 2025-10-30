from multiprocessing import Pool


def count_range(args):
    """Count how many n in the given range satisfy n XOR 2n XOR 3n = 0"""
    start, end = args
    count = 0
    for n in range(start, end):
        if (n ^ (2 * n) ^ (3 * n)) == 0:
            count += 1
    return count


if __name__ == '__main__':
    limit = 2 ** 30
    num_processes = 16
    chunk_size = (limit + num_processes - 1) // num_processes

    # Create ranges for each process
    ranges = [(i * chunk_size, min((i + 1) * chunk_size, limit + 1))
              for i in range(num_processes)]

    # Process ranges in parallel
    with Pool(num_processes) as pool:
        results = pool.map(count_range, ranges)

    # Sum results from all processes
    total = sum(results)
    print(total)