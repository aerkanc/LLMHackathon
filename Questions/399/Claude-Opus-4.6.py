import numpy as np
from multiprocessing import Pool
import math

TARGET = 100_000_000
N_MAX = 160_000_000
B = 5_000_000

_is_p = [True] * 2301
_is_p[0] = _is_p[1] = False
for _i in range(2, 48):
    if _is_p[_i]:
        for _j in range(_i*_i, 2301, _i):
            _is_p[_j] = False
TRIAL_PRIMES = [i for i in range(2, 2301) if _is_p[i]]

def factorize(n):
    factors = {}
    for p in TRIAL_PRIMES:
        if p * p > n:
            break
        while n % p == 0:
            factors[p] = factors.get(p, 0) + 1
            n //= p
    if n > 1:
        factors[n] = 1
    return factors

def sorted_divisors(factors):
    divs = [1]
    for p, e in factors.items():
        new = []
        pe = 1
        for _ in range(e + 1):
            for d in divs:
                new.append(d * pe)
            pe *= p
        divs = new
    divs.sort()
    return divs

def fib_mod(n, m):
    if m == 1:
        return 0
    if n <= 0:
        return 0
    if n <= 2:
        return 1 % m
    a, b = 1, 1
    for i in range(n.bit_length() - 2, -1, -1):
        c = a * (2 * b - a) % m
        d = (a * a + b * b) % m
        if (n >> i) & 1:
            a, b = d, (c + d) % m
        else:
            a, b = c, d
    return a % m

def compute_chunk(primes_list):
    results = []
    for p in primes_list:
        if p == 2:
            results.append((2, 3))
            continue
        if p == 5:
            results.append((5, 5))
            continue
        r = p % 5
        m_val = p - 1 if r == 1 or r == 4 else p + 1
        facts = factorize(m_val)
        divs = sorted_divisors(facts)
        alpha = m_val
        for d in divs:
            if fib_mod(d, p) == 0:
                alpha = d
                break
        results.append((p, alpha))
    return results

def main():
    is_prime = np.ones(B + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(B**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
    primes = np.where(is_prime)[0].tolist()

    n_workers = 16
    chunk_size = (len(primes) + n_workers - 1) // n_workers
    chunks = [primes[i:i+chunk_size] for i in range(0, len(primes), chunk_size)]
    with Pool(n_workers) as pool:
        all_results = pool.map(compute_chunk, chunks)

    bad_divisors = []
    for results in all_results:
        for p, alpha in results:
            m = p * alpha
            if m <= N_MAX:
                bad_divisors.append(m)

    sieve = np.ones(N_MAX + 1, dtype=np.bool_)
    sieve[0] = False
    for m in bad_divisors:
        sieve[m::m] = False

    count = 0
    n_target = -1
    chunk_sz = 10_000_000
    for start in range(1, N_MAX + 1, chunk_sz):
        end = min(start + chunk_sz, N_MAX + 1)
        seg = sieve[start:end]
        seg_count = int(np.sum(seg))
        if count + seg_count >= TARGET:
            cs = np.cumsum(seg)
            idx = int(np.searchsorted(cs, TARGET - count))
            n_target = start + idx
            break
        count += seg_count

    MOD = 10**16
    last16 = fib_mod(n_target, MOD)

    log10_phi = math.log10((1 + math.sqrt(5)) / 2)
    log10_fib = n_target * log10_phi - 0.5 * math.log10(5)
    exponent = int(math.floor(log10_fib))
    frac = log10_fib - exponent
    mantissa = 10.0 ** frac
    mantissa_r = round(mantissa, 1)
    if mantissa_r >= 10.0:
        mantissa_r /= 10.0
        exponent += 1

    last16_str = str(last16).zfill(16)
    print(f"{last16_str},{mantissa_r:.1f}e{exponent}")

if __name__ == '__main__':
    main()