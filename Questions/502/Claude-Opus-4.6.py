import numpy as np

def solve():
    MOD = 10**9 + 7
    K_SPLIT = 1024  # Split base for FFT multiplication

    # ---- Polynomial arithmetic mod z^N mod MOD ----

    def polymul(a, b, N):
        a = np.asarray(a, dtype=np.int64)
        b = np.asarray(b, dtype=np.int64)
        la = min(len(a), N)
        lb = min(len(b), N)
        if la == 0 or lb == 0:
            return np.zeros(N, dtype=np.int64)
        a = a[:la]; b = b[:lb]
        out_len = min(la + lb - 1, N)

        if min(la, lb) <= 200:
            result = np.zeros(out_len, dtype=np.int64)
            if la < lb:
                a, b = b, a
                la, lb = lb, la
            for i in range(lb):
                end = min(la + i, out_len)
                seg = end - i
                if seg > 0:
                    result[i:end] = (result[i:end] + int(b[i]) * a[:seg]) % MOD
            r = np.zeros(N, dtype=np.int64)
            r[:out_len] = result
            return r

        # FFT with 3-way split (K=1024)
        a0 = (a % K_SPLIT).astype(np.float64)
        a1 = ((a // K_SPLIT) % K_SPLIT).astype(np.float64)
        a2 = (a // (K_SPLIT * K_SPLIT)).astype(np.float64)
        b0 = (b % K_SPLIT).astype(np.float64)
        b1 = ((b // K_SPLIT) % K_SPLIT).astype(np.float64)
        b2 = (b // (K_SPLIT * K_SPLIT)).astype(np.float64)

        sz = 1
        while sz < la + lb:
            sz <<= 1

        fa = [np.fft.rfft(x, sz) for x in [a0, a1, a2]]
        fb = [np.fft.rfft(x, sz) for x in [b0, b1, b2]]

        parts = [None] * 5
        for i in range(3):
            for j in range(3):
                p = i + j
                conv = np.round(np.fft.irfft(fa[i] * fb[j], sz)[:out_len]).astype(np.int64)
                conv %= MOD
                if parts[p] is None:
                    parts[p] = conv
                else:
                    parts[p] = (parts[p] + conv) % MOD

        result = np.zeros(out_len, dtype=np.int64)
        Kpow = 1
        for p in range(5):
            if parts[p] is not None:
                result = (result + parts[p] * Kpow) % MOD
            Kpow = Kpow * K_SPLIT % MOD

        r = np.zeros(N, dtype=np.int64)
        r[:out_len] = result
        return r

    def polyadd(a, b, N):
        r = np.zeros(N, dtype=np.int64)
        la = min(len(a), N); lb = min(len(b), N)
        r[:la] = a[:la]
        r[:lb] = (r[:lb] + b[:lb]) % MOD
        return r

    def polysub(a, b, N):
        r = np.zeros(N, dtype=np.int64)
        la = min(len(a), N); lb = min(len(b), N)
        r[:la] = a[:la]
        r[:lb] = (r[:lb] - b[:lb]) % MOD
        return r

    # ---- 2x2 matrix with polynomial entries ----

    def mat2mul(M1, M2, N):
        a1, b1, c1, d1 = M1
        a2, b2, c2, d2 = M2
        return [
            polyadd(polymul(a1, a2, N), polymul(b1, c2, N), N),
            polyadd(polymul(a1, b2, N), polymul(b1, d2, N), N),
            polyadd(polymul(c1, a2, N), polymul(d1, c2, N), N),
            polyadd(polymul(c1, b2, N), polymul(d1, d2, N), N),
        ]

    def mat2pow(M, k, N):
        I = [np.zeros(N, dtype=np.int64) for _ in range(4)]
        I[0][0] = 1; I[3][0] = 1
        result = I
        while k > 0:
            if k & 1:
                result = mat2mul(result, M, N)
            k >>= 1
            if k > 0:
                M = mat2mul(M, M, N)
        return result

    def make_M(N):
        Ma = np.zeros(N, dtype=np.int64); Ma[0] = MOD - 1
        Mb = np.zeros(N, dtype=np.int64); Mb[0] = 2
        Mc = np.zeros(N, dtype=np.int64)
        if N > 1: Mc[1] = 1
        Md = np.zeros(N, dtype=np.int64); Md[0] = 1
        if N > 1: Md[1] = MOD - 2
        return [Ma, Mb, Mc, Md]

    def Bk_PQ_from_Mk(Mk, N):
        a, b, c, d = Mk
        P = polyadd(a, b, N)
        bshift = np.zeros(N, dtype=np.int64)
        if N > 1: bshift[1:] = b[:N-1]
        P = polysub(P, bshift, N)
        Q = polyadd(c, d, N)
        dshift = np.zeros(N, dtype=np.int64)
        if N > 1: dshift[1:] = d[:N-1]
        Q = polysub(Q, dshift, N)
        return P, Q

    def polyinv(q, N):
        q0_inv = pow(int(q[0]), MOD - 2, MOD)
        s = np.zeros(N, dtype=np.int64)
        s[0] = q0_inv
        m = 1
        while m < N:
            m2 = min(m * 2, N)
            qs = polymul(q[:m2], s[:m2], m2)
            two_minus_qs = np.zeros(m2, dtype=np.int64)
            two_minus_qs[0] = 2
            two_minus_qs = polysub(two_minus_qs, qs, m2)
            s_new = polymul(s[:m2], two_minus_qs, m2)
            s = np.zeros(N, dtype=np.int64)
            s[:m2] = s_new[:m2]
            m = m2
        return s

    # ---- Get [z^w] B_k via power series ----

    def get_Bk_coeff(k, w):
        N = w + 1
        M = make_M(N)
        Mk = mat2pow(M, k, N)
        P, Q = Bk_PQ_from_Mk(Mk, N)
        Qinv = polyinv(Q, N)
        B = polymul(P, Qinv, N)
        return int(B[w]) % MOD

    # ---- Get [z^w] B_k for large w via linear recurrence ----

    def get_Bk_coeff_large_w(k, w):
        N = k + 2
        M = make_M(N)
        Mk = mat2pow(M, k, N)
        P, Q = Bk_PQ_from_Mk(Mk, N)

        degQ = N - 1
        while degQ > 0 and Q[degQ] == 0: degQ -= 1
        degP = N - 1
        while degP > 0 and P[degP] == 0: degP -= 1

        d = degQ
        if d == 0:
            return int(P[0]) * pow(int(Q[0]), MOD - 2, MOD) % MOD if w == 0 else 0

        q0_inv = pow(int(Q[0]), MOD - 2, MOD)

        # Compute initial d values of B = P/Q
        b = [0] * d
        for n in range(d):
            s = int(P[n]) if n <= degP else 0
            for j in range(1, min(n + 1, degQ + 1)):
                s = (s - int(Q[j]) * b[n - j]) % MOD
            b[n] = s * q0_inv % MOD

        if w < d:
            return b[w]

        # Companion matrix for the linear recurrence
        c = [(-int(Q[j]) * q0_inv) % MOD for j in range(1, d + 1)]

        C = np.zeros((d, d), dtype=np.int64)
        for j in range(d):
            C[0][j] = c[j]
        for i in range(1, d):
            C[i][i - 1] = 1

        S = 1 << 15

        def matmul_mod(A, B):
            A_lo = A % S
            A_hi = A // S
            C_lo = A_lo @ B % MOD
            C_hi = A_hi @ B % MOD
            return (C_lo + C_hi * S) % MOD

        steps = w - d + 1
        result = np.eye(d, dtype=np.int64)
        base = C.copy()
        while steps > 0:
            if steps & 1:
                result = matmul_mod(result, base)
            steps >>= 1
            if steps > 0:
                base = matmul_mod(base, base)

        state = np.array([b[d - 1 - i] for i in range(d)], dtype=np.int64)
        # ans = result[0] . state
        prods = result[0] * state % MOD
        ans = int(np.sum(prods) % MOD)
        return ans

    # ---- Compute F(w, h) ----

    def compute_F(w, h):
        inv2 = pow(2, MOD - 2, MOD)
        hw = pow(h, w, MOD)
        h1w = pow(h - 1, w, MOD)

        if w > 2 * h + 10:
            # Large w, moderate h: use linear recurrence approach
            Rh1 = get_Bk_coeff_large_w(h - 1, w)
            Rh2 = get_Bk_coeff_large_w(h - 2, w)
        else:
            # Moderate/small w: use power series approach
            Rh1 = get_Bk_coeff(h - 1, w)
            Rh2 = get_Bk_coeff(h - 2, w)

        F = (hw - h1w - Rh1 + Rh2) % MOD * inv2 % MOD
        return F

    # ---- Verify with test cases (all compared mod MOD) ----
    test = compute_F(4, 2)
    assert test == 10, f"F(4,2) = {test}, expected 10"

    test2 = compute_F(13, 10)
    assert test2 == 3729050610636 % MOD, f"F(13,10) = {test2}, expected {3729050610636 % MOD}"

    test3 = compute_F(10, 13)
    assert test3 == 37959702514 % MOD, f"F(10,13) = {test3}, expected {37959702514 % MOD}"

    test4 = compute_F(100, 100)
    assert test4 == 841913936, f"F(100,100) = {test4}, expected 841913936"

    # ---- Compute the answer ----
    F1 = compute_F(10**12, 100)
    F2 = compute_F(10000, 10000)
    F3 = compute_F(100, 10**12)

    answer = (F1 + F2 + F3) % MOD
    print(answer)

solve()