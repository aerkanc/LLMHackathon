import numpy as np


def main():
    # Read the matrix from file
    with open('"./0081_matrix.txt"', 'r') as f:
        lines = f.readlines()

    # Parse the matrix
    matrix = []
    for line in lines:
        row = [int(x) for x in line.strip().split(',')]
        matrix.append(row)

    # Convert to numpy array for efficient operations
    grid = np.array(matrix, dtype=np.int64)
    n = grid.shape[0]

    # Initialize DP table
    dp = np.zeros((n, n), dtype=np.int64)
    dp[0, 0] = grid[0, 0]

    # Fill first row (can only come from left)
    for j in range(1, n):
        dp[0, j] = dp[0, j - 1] + grid[0, j]

    # Fill first column (can only come from top)
    for i in range(1, n):
        dp[i, 0] = dp[i - 1, 0] + grid[i, 0]

    # Fill rest of the DP table
    for i in range(1, n):
        for j in range(1, n):
            dp[i, j] = min(dp[i - 1, j], dp[i, j - 1]) + grid[i, j]

    print(dp[n - 1, n - 1])


if __name__ == "__main__":
    main()