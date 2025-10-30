import numpy as np
import sys


def find_largest_exponential_line():
    """
    Solves the Project Euler Problem 99 by finding the line number
    with the largest exponential value.

    It compares b * log(a) for each line (a, b) in the file.
    """
    try:
        # Load the data from 'base_exp.txt'.
        # This file is expected to be in the same directory.
        # np.loadtxt is highly optimized for reading text files with numerical data.
        # It will return a 2D array, where each row is [base, exponent].
        data = np.loadtxt('base_exp.txt', delimiter=',')

        # data[:, 0] is the column of bases (a)
        # data[:, 1] is the column of exponents (b)

        # Calculate the log values: b * log(a)
        # np.log is the natural logarithm (ln), which is applied element-wise.
        # This is a fast, vectorized operation.
        log_values = data[:, 1] * np.log(data[:, 0])

        # np.argmax finds the 0-based index of the maximum value in the array.
        max_index = np.argmax(log_values)

        # The problem asks for the line number, which is 1-based.
        # We add 1 to the 0-based index to get the line number.
        result = max_index + 1

        # Print only the final numerical result as required.
        print(result)

    except FileNotFoundError:
        # Per the instructions, we should not print debug or error messages,
        # only the final result. In a real-world scenario, we would
        # print an error message to sys.stderr.
        # print("Error: 'base_exp.txt' not found.", file=sys.stderr)
        pass  # Fail silently
    except Exception as e:
        # Handle other potential errors (e.g., file format issues) silently.
        # print(f"An error occurred: {e}", file=sys.stderr)
        pass  # Fail silently


if __name__ == "__main__":
    find_largest_exponential_line()
