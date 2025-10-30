import numpy as np
import sys


def solve_path_sum():
    """
    Reads an 80x80 matrix from 'matrix.txt', computes the minimal
    path sum from top-left to bottom-right moving only right and down,
    and prints the final sum.
    """

    # Set the file name for the input matrix
    FILE_NAME = './0081_matrix.txt'

    try:
        # Load the matrix from the text file using numpy.
        # We specify dtype=np.int64 to handle large sums, although
        # the final sum should fit within a 32-bit integer.
        # np.loadtxt is highly efficient for reading delimited numerical data.
        matrix = np.loadtxt(FILE_NAME, delimiter=',', dtype=np.int64)
    except IOError:
        # In a real-world script, we'd handle this.
        # In this contest setting, if the file is missing,
        # the script is expected to fail. We will not print
        # any error messages, as per the rules.
        return
    except Exception:
        # Catch other potential loading errors
        return

    # Get the size of the matrix (assumed to be N x N)
    n = matrix.shape[0]

    if n == 0:
        # Handle empty matrix case
        return

    # --- Begin Dynamic Programming ---

    # 1. Fill the first row.
    # Each cell's minimal path sum is its value plus the sum of the cell to its left.
    # np.add.accumulate computes the cumulative sum in-place, which is
    # equivalent to:
    # for j in range(1, n):
    #     matrix[0, j] += matrix[0, j-1]
    np.add.accumulate(matrix[0, :], out=matrix[0, :])

    # 2. Fill the first column.
    # Each cell's minimal path sum is its value plus the sum of the cell above it.
    # np.add.accumulate on the column view (a slice) achieves this.
    # equivalent to:
    # for i in range(1, n):
    #     matrix[i, 0] += matrix[i-1, 0]
    np.add.accumulate(matrix[:, 0], out=matrix[:, 0])

    # 3. Fill the rest of the matrix.
    # For each cell (i, j), the minimal path sum is its own value
    # plus the minimum of the path sum from above (i-1, j) or
    # from the left (i, j-1).
    for i in range(1, n):
        for j in range(1, n):
            matrix[i, j] += min(matrix[i - 1, j], matrix[i, j - 1])

    # --- End Dynamic Programming ---

    # The final answer is the minimal path sum stored in the
    # bottom-right corner cell (n-1, n-1).
    final_sum = matrix[n - 1, n - 1]

    # Print *only* the final numerical result to stdout.
    print(final_sum)


if __name__ == "__main__":
    # Set recursion depth higher just in case, although not needed for this iterative DP
    sys.setrecursionlimit(2000)
    solve_path_sum()
