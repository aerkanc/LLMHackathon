import math
import bisect
from multiprocessing import Pool

N = 10_000_000


def sieve(n):
    is_prime = bytearray(b'\x01') * (n + 1)
    is_prime[0] = is_prime[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            is_prime[i * i::i] = bytearray(len(is_prime[i * i::i]))
    return [i for i in range(2, n + 1) if is_prime[i]]


primes = []
prime_prefix_sum = []


def compute_for_p(p):
    total = 0
    start = bisect.bisect_right(primes, p)
    max_q = N // p
    end = bisect.bisect_right(primes, max_q)

    if start >= end:
        return 0

    # Threshold: largest q where p^2*q <= N OR p*q^2 <= N
    t1 = N // (p * p)
    t2 = math.isqrt(N // p)
    # Be safe: also check (t2+1)
    if p * (t2 + 1) * (t2 + 1) <= N:
        t2 += 1
    threshold = max(t1, t2)

    # Simple pairs: q > threshold, M = p*q
    simple_start = bisect.bisect_right(primes, threshold)
    simple_start = max(simple_start, start)
    if simple_start < end:
        simple_sum = prime_prefix_sum[end] - prime_prefix_sum[simple_start]
        total += p * simple_sum

    # Complex pairs: q from start to min(simple_start, end) - 1
    complex_end = min(simple_start, end)
    for i in range(start, complex_end):
        q = primes[i]
        best = 0
        qb = q
        while True:
            limit = N // qb
            if limit < p:
                break
            pa = p
            while pa <= limit // p:
                pa *= p
            val = pa * qb
            if val > best:
                best = val
            if qb > N // q:
                break
            qb *= q
        total += best

    return total


def main():
    global primes, prime_prefix_sum
    primes = sieve(N // 2)

    prime_prefix_sum = [0] * (len(primes) + 1)
    for i, p in enumerate(primes):
        prime_prefix_sum[i + 1] = prime_prefix_sum[i] + p

    valid_p = []
    for p in primes:
        if p * p >= N:
            break
        valid_p.append(p)

    with Pool(16) as pool:
        results = pool.map(compute_for_p, valid_p, chunksize=1)

    print(sum(results))


if __name__ == '__main__':
    main()