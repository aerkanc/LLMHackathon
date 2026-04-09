import math
import multiprocessing as mp

MOD = 10 ** 9
N = 10 ** 11


def compute_sigma(x: int) -> int:
    """Return Σ(x) = ∑_{k=1}^x σ(k) modulo MOD."""
    res = 0
    i = 1
    while i <= x:
        q = x // i
        j = x // q
        cnt = j - i + 1
        sum_i = (i + j) * cnt // 2
        res = (res + sum_i * q) % MOD
        i = j + 1
    return res


def precompute_mu(limit: int):
    """Linear sieve for μ up to limit. Returns μ, μ·id and list of indices with μ≠0 (starting from 2)."""
    mu = [0] * (limit + 1)
    mu[1] = 1
    primes = []
    is_comp = [False] * (limit + 1)
    for i in range(2, limit + 1):
        if not is_comp[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            ip = i * p
            if ip > limit:
                break
            is_comp[ip] = True
            if i % p == 0:
                mu[ip] = 0
                break
            else:
                mu[ip] = -mu[i]

    mu_d = [0] * (limit + 1)
    valid = []
    for i in range(1, limit + 1):
        mu_d[i] = mu[i] * i
        if i >= 2 and mu[i] != 0:
            valid.append(i)
    return mu, mu_d, valid


def precompute_sigma_small(limit: int):
    """Compute Σ(x) for x=0..limit by divisor sum sieve."""
    sigma = [0] * (limit + 1)
    for i in range(1, limit + 1):
        for j in range(i, limit + 1, i):
            sigma[j] = (sigma[j] + i) % MOD
    Sigma = [0] * (limit + 1)
    for i in range(1, limit + 1):
        Sigma[i] = (Sigma[i - 1] + sigma[i]) % MOD
    return Sigma


def main():
    sqrtN = math.isqrt(N)

    # ----- precomputation for μ and small Σ -----
    mu, mu_d, valid_d = precompute_mu(sqrtN)
    Sigma_small = precompute_sigma_small(sqrtN)

    # T(n) = n(n+1)/2 modulo MOD for n ≤ sqrtN
    T_mod = [0] * (sqrtN + 1)
    for i in range(1, sqrtN + 1):
        T_mod[i] = i * (i + 1) // 2 % MOD

    # ----- large values x = floor(N / i) -----
    large_set = {N // i for i in range(1, sqrtN + 1)}
    large_list = sorted(large_set)                     # all distinct, sorted

    # compute Σ(x) for all large x in parallel
    with mp.Pool(processes=mp.cpu_count()) as pool:
        sigma_res = pool.map(compute_sigma, large_list)
    large_sigma = dict(zip(large_list, sigma_res))

    # ----- all x for which M(x) is needed -----
    all_x = sorted(set(range(1, sqrtN + 1)) | large_set)

    # ----- M(x) = ∑_{d=1}^{x} μ(d)·d modulo MOD -----
    M_dict = {}

    # small x (≤ sqrtN) from prefix sums
    M_small = [0] * (sqrtN + 1)
    for i in range(1, sqrtN + 1):
        M_small[i] = (M_small[i - 1] + mu_d[i]) % MOD
    for x in range(1, sqrtN + 1):
        M_dict[x] = M_small[x]

    # process larger x in increasing order
    for x in all_x:
        if x <= sqrtN:
            continue
        m = x
        half = m // 2
        M_half = M_dict[half]
        limit = math.isqrt(m)

        # direct part: d = 2 .. limit, μ(d) ≠ 0
        S = 0
        for d in valid_d:
            if d > limit:
                break
            t = m // d
            S = (S + mu_d[d] * T_mod[t]) % MOD

        # grouped part: d > limit, grouped by t = floor(m/d)
        t_max = m // (limit + 1)          # t runs from 2 to t_max
        for t in range(2, t_max + 1):
            a = m // (t + 1) + 1
            b = m // t
            d_low = max(a, limit + 1)
            d_high = min(b, half)
            if d_low <= d_high:
                M_high = M_dict[d_high]
                M_low = M_dict.get(d_low - 1, 0)
                diff = (M_high - M_low) % MOD
                S = (S + T_mod[t] * diff) % MOD

        T_m = (m * (m + 1) // 2) % MOD
        M_val = (M_half + 1 - T_m - S) % MOD
        M_dict[m] = M_val

    # ----- final sum S(N) = ∑ μ(d)d·Σ(N/d)² + ∑ Σ(q)²·(M(N/q)-M(N/(q+1))) -----
    total = 0
    # first sum: d = 1 .. sqrtN
    for d in range(1, sqrtN + 1):
        x = N // d
        sigma_val = large_sigma[x]          # x is in large_set
        term = mu_d[d] * (sigma_val * sigma_val % MOD) % MOD
        total = (total + term) % MOD

    # second sum: q = 1 .. sqrtN
    for q in range(1, sqrtN + 1):
        sigma_q = Sigma_small[q]
        term = sigma_q * sigma_q % MOD
        M1 = M_dict[N // q]
        M2 = M_dict[N // (q + 1)]
        diff = (M1 - M2) % MOD
        total = (total + term * diff) % MOD

    print(total)


if __name__ == "__main__":
    main()