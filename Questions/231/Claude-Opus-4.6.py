import numpy as np

def solve():
    N = 20_000_000
    K = 15_000_000
    M = N - K  # 5_000_000

    # Sieve of Eratosthenes up to N
    sieve = np.ones(N + 1, dtype=bool)
    sieve[0] = sieve[1] = False
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = False

    primes = np.nonzero(sieve)[0]

    threshold = int(N**0.5) + 1  # ~4473

    small_primes = primes[primes <= threshold]
    large_primes = primes[primes > threshold]

    # Large primes: p^2 > N so only one term in Legendre sum
    lp = large_primes.astype(np.int64)
    exp1 = N // lp - K // lp - M // lp
    total = int(np.sum(lp * exp1))

    # Small primes: need multiple powers
    for p in small_primes:
        p = int(p)
        exp = 0
        pk = p
        while pk <= N:
            exp += N // pk - K // pk - M // pk
            pk *= p
        total += p * exp

    print(total)

solve()