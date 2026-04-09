import sys
from multiprocessing import Pool

MOD = 10 ** 9


def compute_H_exact(x):
    """Computes H(x) using the block trick for numbers > B independent of sieve"""
    ans = 0
    l = 1
    while l <= x:
        v = x // l
        r = x // v
        # sum of integers from l to r
        sum_a = (r - l + 1) * (l + r) // 2
        sum_a %= MOD
        ans = (ans + sum_a * v) % MOD
        l = r + 1
    return x, ans % MOD


def solve():
    N = 10 ** 11
    B = 10_000_000

    is_prime = bytearray(b'\x01') * (B + 1)
    primes = []
    mu = [0] * (B + 1)
    sigma = [0] * (B + 1)
    low = [0] * (B + 1)

    mu[1] = 1
    sigma[1] = 1

    # 1. Linear Sieve Execution
    append = primes.append
    for i in range(2, B + 1):
        if is_prime[i]:
            append(i)
            mu[i] = -1
            sigma[i] = i + 1
            low[i] = i
        for p in primes:
            ip = i * p
            if ip > B:
                break
            is_prime[ip] = 0
            if i % p == 0:
                mu[ip] = 0
                low[ip] = low[i] * p
                if low[i] == i:
                    sigma[ip] = (sigma[i] * p + 1) % MOD
                else:
                    sigma[ip] = (sigma[i // low[i]] * sigma[low[ip]]) % MOD
                break
            else:
                mu[ip] = -mu[i]
                low[ip] = p
                sigma[ip] = (sigma[i] * (p + 1)) % MOD

    pref_M = mu
    pref_H = sigma

    pref_M[0] = 0
    pref_H[0] = 0

    # Cascade to Prefix Sums in-place to save memory
    for i in range(2, B + 1):
        pref_M[i] = (pref_M[i - 1] + pref_M[i] * i) % MOD
        pref_H[i] = (pref_H[i - 1] + pref_H[i]) % MOD

    memo_M = [None] * (N // B + 2)
    memo_H = [None] * (N // B + 2)

    # 2. Parallelized Block Trick evaluations for elements strictly outside the Sieve
    req_K = set()
    for l in range(1, N // B + 1):
        K = N // l
        if K > B:
            req_K.add(K)

    with Pool() as pool:
        results = pool.map(compute_H_exact, list(req_K), chunksize=100)

    for x, val in results:
        memo_H[N // x] = val

    def get_M(x):
        if x <= B:
            return pref_M[x]

        idx = N // x
        if memo_M[idx] is not None:
            return memo_M[idx]

        ans = 1
        l = 2
        while l <= x:
            v = x // l
            r = x // v
            sum_k = (r - l + 1) * (l + r) // 2
            sum_k %= MOD
            ans = (ans - sum_k * get_M(v)) % MOD
            l = r + 1

        ans %= MOD
        memo_M[idx] = ans
        return ans

    def get_H(x):
        if x <= B:
            return pref_H[x]
        return memo_H[N // x]

    # 3. Final Integration Loop
    ans = 0
    l = 1
    while l <= N:
        K = N // l
        r = N // K
        hk = get_H(K)
        mk_sum = (get_M(r) - get_M(l - 1)) % MOD
        ans = (ans + hk * hk % MOD * mk_sum) % MOD
        l = r + 1

    print(ans)


if __name__ == '__main__':
    solve()