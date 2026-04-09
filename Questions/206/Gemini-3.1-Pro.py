import multiprocessing


def check_range(start, end):
    # Iterate by 10s and check numbers ending in 3 and 7
    for i in range(start, end, 10):
        # Check y ending in 3
        v1 = i + 3
        if str(v1 * v1)[::2] == '123456789':
            return v1 * 10

        # Check y ending in 7
        v2 = i + 7
        if str(v2 * v2)[::2] == '123456789':
            return v2 * 10

    return None


def main():
    start_val = 101010100
    end_val = 138902670

    # Utilizing all available CPU cores to speed up the brute-force search
    num_processes = multiprocessing.cpu_count()
    if num_processes < 1:
        num_processes = 1

    step = (end_val - start_val) // num_processes
    # Ensure our step size keeps the boundaries aligned to multiples of 10
    step = (step // 10) * 10
    if step == 0:
        step = 10

    ranges = []
    curr = start_val
    for i in range(num_processes):
        next_curr = curr + step if i < num_processes - 1 else end_val
        ranges.append((curr, next_curr))
        curr = next_curr

    # Execute concurrent searches across the partitioned numerical ranges
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(check_range, ranges)
        for res in results:
            if res is not None:
                print(res)
                # Terminate early once the unique integer is found
                return


if __name__ == '__main__':
    main()