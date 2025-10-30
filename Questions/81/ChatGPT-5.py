# Project Euler style problem (Path Sum: Two Ways)
# Compute the minimal path sum from top-left to bottom-right in an integer matrix,
# moving only right and down. The matrix is expected to be in "matrix.txt" with
# comma-separated values (80x80 in the original problem).
#
# The program prints ONLY the final minimal sum.

import os
import re
import sys
import numpy as np

def find_matrix_file():
    # Prefer the canonical filename if present
    preferred = "./0081_matrix.txt"
    if os.path.isfile(preferred):
        return preferred

    # Otherwise, look for a likely candidate: any .txt containing digits and commas
    candidates = []
    for fname in os.listdir("."):
        if fname.lower().endswith(".txt") and os.path.isfile(fname):
            try:
                with open(fname, "r", encoding="utf-8") as f:
                    head = f.read(4096)
                if re.search(r"\d", head) and ("," in head or "\n" in head):
                    candidates.append((os.path.getsize(fname), fname))
            except Exception:
                continue
    if candidates:
        # Choose the largest plausible text file (original is ~31KB)
        candidates.sort(reverse=True)
        return candidates[0][1]

    # Also try common mounted data paths (e.g., /mnt/data)
    try_paths = ["/mnt/data/matrix.txt", "/mnt/data/81_matrix.txt"]
    for p in try_paths:
        if os.path.isfile(p):
            return p

    raise FileNotFoundError(
        "matrix.txt not found. Please ensure the matrix file is present in the working directory."
    )

def load_matrix(path):
    # Robust load for comma-separated integers
    try:
        return np.loadtxt(path, delimiter=",", dtype=np.int64)
    except Exception:
        # Fallback manual parsing
        rows = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rows.append([int(x) for x in line.split(",")])
        return np.array(rows, dtype=np.int64)

def minimal_path_sum_right_down(grid: np.ndarray) -> int:
    # Dynamic programming: dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
    # Operate in a separate array to keep intent clear (memory is plentiful).
    dp = grid.copy()

    # Initialize first row and first column
    dp[0, 1:] = np.cumsum(dp[0, 1:], dtype=np.int64) + dp[0, 0]
    dp[1:, 0] = np.cumsum(dp[1:, 0], dtype=np.int64) + 0  # will add progressively below
    # The above set dp[0,*]. For first column, we need cumulative sum including dp[0,0].
    for i in range(1, dp.shape[0]):
        dp[i, 0] = dp[i - 1, 0] + grid[i, 0]

    # Fill remaining cells
    rows, cols = dp.shape
    for i in range(1, rows):
        # Row-wise fill; inner loop is small (<=80), fast enough
        for j in range(1, cols):
            up = dp[i - 1, j]
            left = dp[i, j - 1]
            dp[i, j] = grid[i, j] + (up if up < left else left)

    return int(dp[-1, -1])

def main():
    path = find_matrix_file()
    grid = load_matrix(path)
    result = minimal_path_sum_right_down(grid)
    print(result)

if __name__ == "__main__":
    main()
