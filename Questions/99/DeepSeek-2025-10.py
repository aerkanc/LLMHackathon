import math
import multiprocessing as mp
import numpy as np


def process_line(line_data):
    """Process a single line and return (log_value, line_number)"""
    line, line_num = line_data
    base, exponent = map(int, line.strip().split(','))
    # Use logarithm to avoid computing huge numbers
    # log(base^exponent) = exponent * log(base)
    log_value = exponent * math.log(base)
    return (log_value, line_num)


def main():
    # Read the file
    with open('base_exp.txt', 'r') as f:
        lines = f.readlines()

    # Prepare data for parallel processing: (line_content, line_number)
    # Line numbers start from 1
    line_data = [(line, i + 1) for i, line in enumerate(lines)]

    # Use all available CPU cores for parallel processing
    num_cores = mp.cpu_count()

    # Process lines in parallel
    with mp.Pool(processes=num_cores) as pool:
        results = pool.map(process_line, line_data)

    # Find the line with maximum value
    max_log_value, max_line_num = max(results)

    print(max_line_num)


if __name__ == '__main__':
    main()