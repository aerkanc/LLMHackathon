import os


def solve():
    # Account for potential filename variations in the evaluation environment
    candidates = ['./0081_matrix.txt', 'matrix.txt']
    matrix_path = None
    for c in candidates:
        if os.path.exists(c):
            matrix_path = c
            break

    if not matrix_path:
        raise FileNotFoundError("Could not find the matrix file.")

    # Read and parse the matrix
    with open(matrix_path, 'r') as f:
        content = f.read()

    # Clean potential artifacts from file upload strings
    content = content.replace('', '')
    lines = content.strip().split('\n')

    grid = [list(map(int, line.split(','))) for line in lines if line.strip()]
    n = len(grid)
    m = len(grid[0])

    # Dynamic Programming: Update grid in-place to store the minimal path sum to each cell
    for i in range(n):
        for j in range(m):
            if i == 0 and j == 0:
                continue
            elif i == 0:
                # Top row can only be reached from the left
                grid[i][j] += grid[i][j - 1]
            elif j == 0:
                # Leftmost column can only be reached from above
                grid[i][j] += grid[i - 1][j]
            else:
                # Any other cell takes the minimum of the path from above or the path from the left
                grid[i][j] += min(grid[i - 1][j], grid[i][j - 1])

    # The bottom-right cell contains the minimal path sum
    print(grid[n - 1][m - 1])


if __name__ == '__main__':
    solve()