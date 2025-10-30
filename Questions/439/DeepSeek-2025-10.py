import math
from multiprocessing import Pool

MOD = 10 ** 9
N = 10 ** 11


def T1(n):
    a = n
    b = n + 1
    if a % 2 == 0:
        a //= 2
    else:
        b //= 2
    return (a % MOD) * (b % MOD) % MOD


def main():
    M_set = set()
    i = 1
    while i <= N:
        m = N // i
        M_set.add(m)
        i = N // m + 1
    M_list = sorted(M_set)

    def compute_F(m):
        total_F = 0
        i = 1
        while i <= m:
            t = m // i
            j = m // t
            s = (T1(j) - T1(i - 1)) % MOD
            total_F = (total_F + t * s) % MOD
            i = j + 1
        return (m, total_F % MOD)

    F_dict = {}
    with Pool() as pool:
        results = pool.map(compute_F, M_list)
    for m, val in results:
        F_dict[m] = val

    def compute_T2(m):
        total_T2 = 0
        i = 1
        while i <= m:
            t = m // i
            j = m // t
            count = j - i + 1
            total_T2 = (total_T2 + T1(t) * count) % MOD
            i = j + 1
        return (m, total_T2 % MOD)

    T2_dict = {}
    with Pool() as pool:
        results = pool.map(compute_T2, M_list)
    for m, val in results:
        T2_dict[m] = val

    H_dict = {0: 0}
    for m in M_list:
        if m == 0:
            continue
        total_H = 1
        k = 2
        while k <= m:
            t = m // k
            j = m // t
            s = (T1(j) - T1(k - 1)) % MOD
            term = s * H_dict[t] % MOD
            total_H = (total_H - term) % MOD
            k = j + 1
        H_dict[m] = total_H % MOD

    S = 0
    g_min = 1
    while g_min <= N:
        m = N // g_min
        g_max = N // m
        H_g_max = H_dict[g_max]
        H_g_min_minus = H_dict.get(g_min - 1, 0)
        term = (H_g_max - H_g_min_minus) % MOD
        term = term * F_dict[m] % MOD
        term = term * T2_dict[m] % MOD
        S = (S + term) % MOD
        g_min = g_max + 1

    print(S % MOD)


if __name__ == '__main__':
    main()