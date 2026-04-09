from math import factorial

N = 18

# For a digit used c times, the weight is 1 / c! for c = 0..3.
# Scale by 6 (= 3!) to keep everything integral:
# 6 * (1/c!) -> [6, 6, 3, 1]
F = [6, 6, 3, 1]

# The leading digit cannot be zero.
# If digit 0 is used c times in total, its contribution is (N - c) / c!
# Scaling again by 6 gives:
# 6 * ((N-c)/c!) for c = 0..3
G = [6 * (N - c) // factorial(c) for c in range(4)]

# Compute coefficients of F(x)^9 up to degree N.
poly = [0] * (N + 1)
poly[0] = 1

for _ in range(9):
    new_poly = [0] * (N + 1)
    for i, a in enumerate(poly):
        if a == 0:
            continue
        for c, b in enumerate(F):
            j = i + c
            if j <= N:
                new_poly[j] += a * b
    poly = new_poly

# Coefficient of x^N in G(x) * F(x)^9, still scaled by 6^10.
scaled_coeff = 0
for c, gc in enumerate(G):
    if N - c >= 0:
        scaled_coeff += gc * poly[N - c]

# Undo the scaling and multiply by (N-1)! = 17!
answer = factorial(N - 1) * scaled_coeff // (6 ** 10)

print(answer)