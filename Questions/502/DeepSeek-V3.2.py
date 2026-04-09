import sys
import numpy as np

MOD = 1_000_000_007
INV2 = (MOD + 1) // 2          # modular inverse of 2

# ------------------------------------------------------------
# iterative DP using numpy (for moderate H and w)
def total_even_iter(H, w):
    """return total_even(H,w) = number of sequences of length w
       over {1..H} with even total blocks"""
    if H == 0:
        return 0
    # B1[h] = 1 if h even else -1 (mod MOD)
    B = np.zeros(H, dtype=np.int64)
    for h in range(1, H+1):
        B[h-1] = 1 if (h % 2 == 0) else MOD-1

    # sign_x = (-1)^x  (x = height)
    sign = np.where((np.arange(1, H+1) % 2 == 0), 1, MOD-1).astype(np.int64)

    total_seq = pow(H, w, MOD)
    if w == 1:
        total_B = np.sum(B) % MOD
        return (total_seq + total_B) * INV2 % MOD

    # pre‑allocate working arrays
    pref = np.empty(H, dtype=np.int64)
    U = np.empty(H, dtype=np.int64)
    B_next = np.empty(H, dtype=np.int64)
    tmp = np.empty(H, dtype=np.int64)

    for _ in range(2, w+1):
        np.cumsum(B, out=pref)                     # prefix sums of B
        np.multiply(B, sign, out=tmp)              # B * sign
        np.cumsum(tmp, out=U)                      # prefix sums of B*sign
        total_B = pref[-1]                         # total sum of B (exact)
        # B_next = sign * U + (total_B - pref)
        np.multiply(sign, U, out=B_next)
        np.add(B_next, total_B - pref, out=B_next)
        np.mod(B_next, MOD, out=B_next)
        # swap buffers for next iteration
        B, B_next = B_next, B

    total_B = np.sum(B) % MOD
    return (total_seq + total_B) * INV2 % MOD

# ------------------------------------------------------------
# matrix exponentiation (for small H, huge w)
def mat_mul(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        Ci = C[i]
        for k in range(n):
            aik = Ai[k]
            if aik:
                Bk = B[k]
                for j in range(n):
                    Ci[j] = (Ci[j] + aik * Bk[j]) % MOD
    return C

def mat_vec_mul(A, v):
    n = len(A)
    res = [0]*n
    for i in range(n):
        total = 0
        Ai = A[i]
        for j in range(n):
            total = (total + Ai[j] * v[j]) % MOD
        res[i] = total
    return res

def build_matrix_B(H):
    """build H×H matrix M such that B_{next} = M * B"""
    M = [[0]*H for _ in range(H)]
    for y in range(H):
        for x in range(H):
            if x <= y:
                diff = y - x
                M[y][x] = 1 if (diff % 2 == 0) else MOD-1
            else:
                M[y][x] = 1
    return M

def total_even_matrix(H, w):
    if H == 0:
        return 0
    # initial vector B1
    B1 = [0]*H
    for h in range(1, H+1):
        B1[h-1] = 1 if (h % 2 == 0) else MOD-1

    M = build_matrix_B(H)
    exp = w - 1
    vec = B1[:]
    while exp:
        if exp & 1:
            vec = mat_vec_mul(M, vec)
        M = mat_mul(M, M)
        exp >>= 1
    total_B = sum(vec) % MOD
    total_seq = pow(H, w, MOD)
    return (total_seq + total_B) * INV2 % MOD

# ------------------------------------------------------------
# interpolation for huge H, small w (w = 100)
def total_even_poly(w, H_target):
    """return total_even(H_target, w) using Lagrange interpolation"""
    max_H = 2*w + 1                     # 0 … 2w+1
    vals = [0]*(max_H+1)                # vals[H] = total_even(H,w)
    for H in range(1, max_H+1):
        vals[H] = total_even_iter(H, w)

    even_x = list(range(0, max_H+1, 2))
    even_y = [vals[x] for x in even_x]
    odd_x  = list(range(1, max_H+1, 2))
    odd_y  = [vals[x] for x in odd_x]

    def lagrange(xs, ys, x):
        n = len(xs)
        res = 0
        for i in range(n):
            num = 1
            den = 1
            xi = xs[i]
            yi = ys[i]
            for j in range(n):
                if i == j:
                    continue
                num = num * (x - xs[j]) % MOD
                den = den * (xi - xs[j]) % MOD
            term = yi * num % MOD * pow(den, MOD-2, MOD) % MOD
            res = (res + term) % MOD
        return res

    if H_target % 2 == 0:
        return lagrange(even_x, even_y, H_target)
    else:
        return lagrange(odd_x, odd_y, H_target)

# ------------------------------------------------------------
def solve():
    # case 1: w = 10^12, h = 100
    w1 = 10**12
    h1 = 100
    F1 = (total_even_matrix(h1, w1) - total_even_matrix(h1-1, w1)) % MOD

    # case 2: w = 10000, h = 10000
    w2 = 10000
    h2 = 10000
    F2 = (total_even_iter(h2, w2) - total_even_iter(h2-1, w2)) % MOD

    # case 3: w = 100, h = 10^12
    w3 = 100
    h3 = 10**12
    F3 = (total_even_poly(w3, h3) - total_even_poly(w3, h3-1)) % MOD

    ans = (F1 + F2 + F3) % MOD
    print(ans)

if __name__ == "__main__":
    solve()