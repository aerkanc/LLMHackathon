import math
import os
import urllib.request
import multiprocessing


def compute_log(data):
    """
    Computes the logarithm of the exponential expression.
    data: tuple of (line_num, line_string)
    Returns: tuple of (log_value, line_num)
    """
    line_num, line = data
    line = line.strip()
    if not line:
        return -1, line_num

    # Parse base and exponent
    base, exp = map(int, line.split(','))

    # Calculate exp * log(base) which is equivalent to log(base^exp)
    log_val = exp * math.log(base)
    return log_val, line_num


def main():
    file_path = "./0099_base_exp.txt"

    # Ensure the file exists, if not, download it directly from Project Euler
    if not os.path.exists(file_path):
        alt_path = "p099_base_exp.txt"
        if os.path.exists(alt_path):
            file_path = alt_path
        else:
            url = "https://projecteuler.net/project/resources/p099_base_exp.txt"
            urllib.request.urlretrieve(url, file_path)

    # Read lines from the file
    with open(file_path, 'r') as file:
        lines = [(i, line) for i, line in enumerate(file, 1)]

    # Utilize multi-core capabilities to process the data in parallel
    cpu_cores = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=cpu_cores) as pool:
        results = pool.map(compute_log, lines)

    # Find the line with the maximum calculated log value
    best_val, best_line = max(results, key=lambda x: x[0])

    # Print only the final line number result
    print(best_line)


if __name__ == '__main__':
    main()