import sys
import multiprocessing as mp

MOD = 1000000007


def poly_mul(A, B):
    """Multiplies two polynomials A and B modulo 1000000007."""
    res = [0] * (len(A) + len(B) - 1)
    for i, a in enumerate(A):
        if a == 0:
            continue
        for j, b in enumerate(B):
            res[i + j] = (res[i + j] + a * b) % MOD
    return res


def bostan_mori(P, Q, w):
    """Finds the coefficient of x^w in P(x)/Q(x) using the Bostan-Mori algorithm."""
    while w > 0:
        Q_neg = [q if i % 2 == 0 else (-q % MOD) for i, q in enumerate(Q)]
        U = poly_mul(P, Q_neg)
        V = poly_mul(Q, Q_neg)

        P = [U[i] for i in range(w % 2, len(U), 2)]
        Q = [V[i] for i in range(0, len(V), 2)]
        w //= 2

    return (P[0] * pow(Q[0], -1, MOD)) % MOD if P else 0


def dp_divide(P, Q, w):
    """Computes the coefficient of x^w in P(x)/Q(x) using O(w^2) DP."""
    S = [0] * (w + 1)
    if P:
        S[0] = P[0] % MOD
    len_Q = len(Q)
    len_P = len(P)

    for k in range(1, w + 1):
        acc = 0
        limit = min(k, len_Q - 1)
        for j in range(1, limit + 1):
            acc += Q[j] * S[k - j]

        val = P[k] if k < len_P else 0
        S[k] = (val - acc) % MOD

    return S[w]


def get_U(h, D):
    """
    Computes the polynomial U_h(x) up to degree D where U_h(x) corresponds
    to the modified Fibonacci polynomial related to the configurations parity.
    """
    U = [0] * (D + 1)
    if h == 0:
        return U

    start_m = (h - 1) % 2
    if start_m > D:
        return U

    N_start = (h - 1 + start_m) // 2
    if N_start < start_m:
        return U

    C = 1 if start_m == 0 else (N_start % MOD)
    m = start_m

    while m <= D:
        val = (C * pow(-2, m, MOD)) % MOD
        U[m] = val

        N_m = (h - 1 + m) // 2
        num = ((N_m + 1) % MOD) * ((N_m - m) % MOD) % MOD
        den = (m + 1) * (m + 2) % MOD

        C = C * num % MOD * pow(den, -1, MOD) % MOD
        m += 2

    return U


def get_P_Q(h, D):
    """Generates the rational generating function polynomials P and Q for max height h."""
    Uh = get_U(h, D)
    Uh1 = get_U(h - 1, D)

    P = [0] * (D + 1)
    Q = [0] * (D + 1)

    for m in range(D + 1):
        P[m] = (Uh[m] + Uh1[m]) % MOD
        Q[m] = P[m]
        if m > 0:
            Q[m] = (Q[m] - Uh[m - 1]) % MOD

    while len(P) > 1 and P[-1] == 0: P.pop()
    while len(Q) > 1 and Q[-1] == 0: Q.pop()

    return P, Q


def solve_parity_diff(w, h):
    """Calculates the parity difference of configurations for up to height h."""
    if h == 0:
        return 0

    D = min(w, h)
    P, Q = get_P_Q(h, D)

    if w > 10000:
        res = bostan_mori(P, Q, w)
    else:
        res = dp_divide(P, Q, w)

    return (-res) % MOD


def F(w, h):
    """Returns the total number of exact height valid parity castles."""
    if h < 1:
        return 0

    total_exact = (pow(h, w, MOD) - pow(h - 1, w, MOD)) % MOD

    diff_h = solve_parity_diff(w, h)
    diff_h_1 = solve_parity_diff(w, h - 1)

    diff_exact = (diff_h - diff_h_1) % MOD

    ans = (total_exact + diff_exact) * pow(2, -1, MOD) % MOD
    return ans


def worker(args):
    """Wrapper mapping for parallel processing."""
    w, h = args
    return F(w, h)


if __name__ == '__main__':
    queries = [
        (10 ** 12, 100),
        (10000, 10000),
        (100, 10 ** 12)
    ]

    # Calculate across separate processes utilizing multi-core constraints effectively
    with mp.Pool(processes=min(mp.cpu_count(), 4)) as pool:
        results = pool.map(worker, queries)

    final_answer = sum(results) % MOD
    print(final_answer)