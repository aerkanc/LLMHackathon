MOD = 1_000_000_007
INV2 = (MOD + 1) // 2

# ------------------------------------------------------------
# Small-degree polynomial tools (exact, naive; good for w <= 100)
# ------------------------------------------------------------

def poly_add(a, b, n):
    m = min(n, max(len(a), len(b)))
    res = [0] * m
    for i in range(m):
        res[i] = ((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % MOD
    return res

def poly_mul(a, b, n):
    if not a or not b:
        return []
    res = [0] * min(n, len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        lim = min(len(b), n - i)
        for j in range(lim):
            res[i + j] = (res[i + j] + ai * b[j]) % MOD
    return res

def poly_inv(f, n):
    g = [pow(f[0], MOD - 2, MOD)]
    m = 1
    while m < n:
        m2 = min(2 * m, n)
        fg = poly_mul(f[:m2], g, m2)
        fg += [0] * (m2 - len(fg))
        t = [0] * m2
        t[0] = (2 - fg[0]) % MOD
        for i in range(1, m2):
            t[i] = (-fg[i]) % MOD
        g = poly_mul(g, t, m2)
        g += [0] * (m2 - len(g))
        m = m2
    return g[:n]

def poly_div(num, den, n):
    return poly_mul(num, poly_inv(den, n), n)

def mat_mul(A, B, n):
    return [
        [
            poly_add(poly_mul(A[0][0], B[0][0], n), poly_mul(A[0][1], B[1][0], n), n),
            poly_add(poly_mul(A[0][0], B[0][1], n), poly_mul(A[0][1], B[1][1], n), n),
        ],
        [
            poly_add(poly_mul(A[1][0], B[0][0], n), poly_mul(A[1][1], B[1][0], n), n),
            poly_add(poly_mul(A[1][0], B[0][1], n), poly_mul(A[1][1], B[1][1], n), n),
        ],
    ]

def mat_pow(M, e, n):
    R = [[[1], []], [[], [1]]]
    while e:
        if e & 1:
            R = mat_mul(R, M, n)
        e >>= 1
        if e:
            M = mat_mul(M, M, n)
    return R

def signed_exact_small_w(w, h):
    n = w + 1

    # M for y = -1:
    # c' = -(x + (1+x)c) / (1 - x - x c)
    M = [
        [[MOD - 1, MOD - 1], [0, MOD - 1]],
        [[0, MOD - 1], [1, MOD - 1]],
    ]

    # M^{-1}
    Minv = [
        [[MOD - 1, 1], [0, MOD - 1]],
        [[0, MOD - 1], [1, 1]],
    ]

    P = mat_pow(M, h, n)
    Pm1 = mat_mul(P, Minv, n)

    Bh = poly_div(P[0][1], P[1][1], n)
    Bm1 = poly_div(Pm1[0][1], Pm1[1][1], n)
    return (Bh[w] - Bm1[w]) % MOD

# ------------------------------------------------------------
# q_h construction
# q_0 = 1
# q_1 = 1 - x
# q_{n+1} = (1 + x^2) q_{n-1} - 2x q_n
# Exact signed-height-h generating function:
#   S_h(x) = (-1)^h * x / (q_h(x) q_{h-1}(x))
# ------------------------------------------------------------

def q_pair(h):
    if h == 1:
        return [1], [1, MOD - 1]

    q0 = [1]
    q1 = [1, MOD - 1]

    for _ in range(1, h):
        m = len(q0)
        q2 = [0] * (m + 2)

        # +(1) * q0
        for i, v in enumerate(q0):
            q2[i] = (q2[i] + v) % MOD

        # +(x^2) * q0
        for i, v in enumerate(q0):
            q2[i + 2] = (q2[i + 2] + v) % MOD

        # -2x * q1
        for i, v in enumerate(q1):
            q2[i + 1] = (q2[i + 1] - 2 * v) % MOD

        q0, q1 = q1, q2

    return q0, q1  # q_{h-1}, q_h

# ------------------------------------------------------------
# Small-degree Bostan-Mori (good for h = 100)
# ------------------------------------------------------------

def trim(a):
    while a and a[-1] == 0:
        a.pop()
    return a

def conv_small(a, b):
    if not a or not b:
        return []
    res = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            res[i + j] = (res[i + j] + ai * bj) % MOD
    return res

def bostan_mori(P, Q, n):
    P = trim(P[:])
    Q = trim(Q[:])
    while n:
        Qm = [(c if i % 2 == 0 else (-c) % MOD) for i, c in enumerate(Q)]
        S = conv_small(P, Qm)
        T = conv_small(Q, Qm)
        P = [S[i] for i in range(n & 1, len(S), 2)]
        Q = [T[i] for i in range(0, len(T), 2)]
        n >>= 1
    return P[0] * pow(Q[0], MOD - 2, MOD) % MOD

def signed_exact_large_w_small_h(w, h):
    qm, qh = q_pair(h)
    den = conv_small(qh, qm)
    coeff = bostan_mori([1], den, w - 1)
    if h & 1:
        coeff = (-coeff) % MOD
    return coeff

# ------------------------------------------------------------
# Prefix convolution and inverse-series-by-recurrence
# (good for w = h = 10000)
# ------------------------------------------------------------

def prefix_conv(a, b, n):
    # returns coefficients 0..n of a*b
    res = [0] * (n + 1)
    lb = len(b)
    for i, ai in enumerate(a[:n + 1]):
        if ai == 0:
            continue
        lim = min(lb, n + 1 - i)
        for j in range(lim):
            res[i + j] = (res[i + j] + ai * b[j]) % MOD
    return res

def inv_series_coeffs(d, n):
    # d[0] must be 1 here
    a = [0] * (n + 1)
    a[0] = 1
    for k in range(1, n + 1):
        s = 0
        for i in range(1, k + 1):
            s += d[i] * a[k - i]
        a[k] = (-s) % MOD
    return a

def signed_exact_square_10000():
    h = 10_000
    w = 10_000
    qm, qh = q_pair(h)
    den_prefix = prefix_conv(qh, qm, w - 1)
    inv_den = inv_series_coeffs(den_prefix, w - 1)
    coeff = inv_den[w - 1]
    if h & 1:
        coeff = (-coeff) % MOD
    return coeff

# ------------------------------------------------------------
# Final assembly
# ------------------------------------------------------------

def even_exact(w, h, signed_exact):
    total_exact = (pow(h, w, MOD) - pow(h - 1, w, MOD)) % MOD
    return (total_exact + signed_exact) * INV2 % MOD

term1_signed = signed_exact_small_w(100, 10**12)
term1 = even_exact(100, 10**12, term1_signed)

term2_signed = signed_exact_large_w_small_h(10**12, 100)
term2 = even_exact(10**12, 100, term2_signed)

term3_signed = signed_exact_square_10000()
term3 = even_exact(10_000, 10_000, term3_signed)

print((term1 + term2 + term3) % MOD)