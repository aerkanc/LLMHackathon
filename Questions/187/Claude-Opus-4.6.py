import bisect
import numpy as np

def solve():
    N = 10**8
    limit = N // 2 + 1  # max prime we need

    # Sieve of Eratosthenes using numpy for speed
    sieve = np.ones(limit, dtype=np.bool_)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = False

    primes = np.nonzero(sieve)[0]
    primes_list = primes.tolist()  # for bisect

    count = 0
    for i, p in enumerate(primes_list):
        if p * p >= N:
            break
        # q >= p and p*q < N => q < N/p
        max_q = (N - 1) // p  # p*q < N means q <= (N-1)//p
        # count primes in [p, max_q]
        j = bisect.bisect_right(primes_list, max_q)
        count += j - i

    print(count)

solve()