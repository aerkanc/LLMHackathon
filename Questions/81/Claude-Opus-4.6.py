import numpy as np

matrix = np.loadtxt("./0081_matrix.txt", delimiter=",", dtype=np.int64)
n = matrix.shape[0]

for i in range(n):
    for j in range(n):
        if i == 0 and j == 0:
            continue
        elif i == 0:
            matrix[i][j] += matrix[i][j-1]
        elif j == 0:
            matrix[i][j] += matrix[i-1][j]
        else:
            matrix[i][j] += min(matrix[i-1][j], matrix[i][j-1])

print(matrix[n-1][n-1])