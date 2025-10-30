import sys
import os

# Try to read matrix from file
matrix = None

# Try local file first
if os.path.exists('"./0081_matrix.txt"'):
    try:
        with open('"./0081_matrix.txt"', 'r') as f:
            matrix = []
            for line in f:
                row = [int(x) for x in line.strip().split(',')]
                matrix.append(row)
    except Exception as e:
        pass

# If not found locally, try importing from common locations
if matrix is None:
    import urllib.request

    url = "https://projecteuler.net/project/resources/p081_matrix.txt"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = response.read().decode('utf-8')
        lines = data.strip().split('\n')
        matrix = []
        for line in lines:
            row = [int(x) for x in line.split(',')]
            matrix.append(row)
    except Exception as e:
        pass

# If still not found, exit with error
if matrix is None:
    print("Error: Could not load matrix.txt")
    sys.exit(1)

n = len(matrix)

# Dynamic programming approach for minimal path sum
# dp[i][j] = minimum path sum to reach cell (i, j) from (0, 0)
# We can optimize space by using 1D array since we only need previous row
dp = [0] * n
dp[0] = matrix[0][0]

# Fill first row (can only come from left)
for j in range(1, n):
    dp[j] = dp[j - 1] + matrix[0][j]

# Process remaining rows
for i in range(1, n):
    # First column (can only come from top)
    dp[0] = dp[0] + matrix[i][0]

    # Rest of columns (can come from top or left)
    for j in range(1, n):
        dp[j] = matrix[i][j] + min(dp[j], dp[j - 1])

# The answer is in dp[n-1]
print(dp[n - 1])