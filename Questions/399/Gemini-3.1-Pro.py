import multiprocessing as mp
import numpy as np
from decimal import Decimal, getcontext, ROUND_HALF_UP


def worker(args):
    primes_chunk, n_max = args
    res = []
    res_append = res.append
    # Convert numpy array to python list to ensure optimized native int iterations
    primes_list = primes_chunk.tolist()

    for p in primes_list:
        L = n_max // p
        if L < 3:
            continue

        a = 1
        b = 1
        # The rank of apparition Z(p) bounded dynamically or by L
        for k in range(3, L + 1):
            c = a + b
            if c >= p:
                c -= p
            if not c:  # Found Z(p)
                res_append(p * k)
                break
            a = b
            b = c

    return res


def solve():
    N_MAX = 200_000_000
    limit = N_MAX // 3

    # 1. Fast prime generation via NumPy Boolean Sieve
    sieve = np.ones(limit + 1, dtype=np.bool_)
    sieve[:2] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    primes = np.nonzero(sieve)[0].astype(np.int32)

    # 2. Parallel distribution to find forbidden multiples
    n_cores = mp.cpu_count()

    # Round-robin distribution guarantees perfectly balanced workload across all cores
    chunks = [primes[i::n_cores] for i in range(n_cores)]

    pool = mp.Pool(processes=n_cores)
    results = pool.map(worker, [(chunk, N_MAX) for chunk in chunks])
    pool.close()
    pool.join()

    forbidden = []
    for r in results:
        forbidden.extend(r)

    # 3. Apply gathered constraints to a sieve representing Fibonacci indices
    is_sqfree = np.ones(N_MAX + 1, dtype=np.bool_)
    is_sqfree[0] = False  # F_0 is naturally excluded

    for s in forbidden:
        is_sqfree[s::s] = False

    sqfree_indices = np.nonzero(is_sqfree)[0]

    TARGET = 100_000_000
    if len(sqfree_indices) < TARGET:
        raise ValueError("N_MAX upper bound was too small")

    ans_n = int(sqfree_indices[TARGET - 1])

    # 4. Matrix exponentiation specifically to pull the last 16 digits
    mod = 10 ** 16

    def mat_mul(A, B):
        return [
            [(A[0][0] * B[0][0] + A[0][1] * B[1][0]) % mod, (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % mod],
            [(A[1][0] * B[0][0] + A[1][1] * B[1][0]) % mod, (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % mod]
        ]

    def mat_pow(A, p):
        res = [[1, 0], [0, 1]]
        base = A
        while p > 0:
            if p % 2 == 1:
                res = mat_mul(res, base)
            base = mat_mul(base, base)
            p //= 2
        return res

    T = [[1, 1], [1, 0]]
    if ans_n == 0:
        last_16 = 0
    else:
        last_16 = mat_pow(T, ans_n - 1)[0][0]

    # 5. Scientific notation using highly precise implementation of Binet's formula
    getcontext().prec = 100
    phi = (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)
    log_phi = phi.log10()
    log_sqrt5 = Decimal(5).sqrt().log10()

    log_Fn = Decimal(ans_n) * log_phi - log_sqrt5
    E = int(log_Fn.to_integral_value(rounding='ROUND_FLOOR'))
    frac = log_Fn - Decimal(E)
    M = Decimal(10) ** frac

    # Rounding handling based precisely off instructions
    M_rounded = M.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
    if M_rounded == Decimal('10.0'):
        M_rounded = Decimal('1.0')
        E += 1

    sci_str = f"{M_rounded}e{E}"

    # Required strict format output
    print(f"{last_16:016d},{sci_str}")


if __name__ == '__main__':
    solve()