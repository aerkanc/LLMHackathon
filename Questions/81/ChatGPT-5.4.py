from pathlib import Path

def load_matrix():
    candidates = [
        "matrix.txt",
        "./0081_matrix.txt",
        "p081_matrix.txt",
        "81_matrix.txt",
    ]

    for name in candidates:
        p = Path(name)
        if p.is_file():
            with p.open("r", encoding="utf-8") as f:
                return [list(map(int, line.strip().split(","))) for line in f if line.strip()]

    for p in Path(".").rglob("*matrix*.txt"):
        if p.is_file():
            with p.open("r", encoding="utf-8") as f:
                return [list(map(int, line.strip().split(","))) for line in f if line.strip()]

    for p in Path(".").rglob("0081_matrix.txt"):
        if p.is_file():
            with p.open("r", encoding="utf-8") as f:
                return [list(map(int, line.strip().split(","))) for line in f if line.strip()]

    raise FileNotFoundError("Matrix file not found")

def minimal_path_sum(matrix):
    n = len(matrix)
    m = len(matrix[0])

    dp = [0] * m
    dp[0] = matrix[0][0]

    for j in range(1, m):
        dp[j] = dp[j - 1] + matrix[0][j]

    for i in range(1, n):
        dp[0] += matrix[i][0]
        for j in range(1, m):
            if dp[j] < dp[j - 1]:
                dp[j] = dp[j] + matrix[i][j]
            else:
                dp[j] = dp[j - 1] + matrix[i][j]

    return dp[-1]

matrix = load_matrix()
print(minimal_path_sum(matrix))