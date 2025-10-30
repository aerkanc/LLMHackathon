# Project Euler 347 - compute S(10_000_000)
# Largest integer <= N divisible by exactly two distinct primes p and q.
# We compute smallest prime factors (linear sieve), then scan all n<=N.
# For numbers with exactly two distinct prime factors, update the maximum M(p,q,N).
# Finally sum the distinct maxima.

def sieve_spf(n: int):
    spf = [0] * (n + 1)
    primes = []
    for i in range(2, n + 1):
        if spf[i] == 0:
            spf[i] = i
            primes.append(i)
        si = spf[i]
        for p in primes:
            x = p * i
            if x > n:
                break
            spf[x] = p
            if p == si:
                break
    return spf

def main():
    N = 10_000_000
    spf = sieve_spf(N)

    max_for_pair = {}  # key = (p<<24)|q (since primes < 2^24), value = max n
    get = max_for_pair.get
    for n in range(2, N + 1):
        x = n
        p1 = spf[x]
        if p1 == x:  # prime => only one prime factor
            continue
        # remove all powers of p1
        while x % p1 == 0:
            x //= p1
        if x == 1:
            continue  # only one distinct prime factor
        p2 = spf[x]
        # remove all powers of p2
        while x % p2 == 0:
            x //= p2
        if x != 1:
            continue  # more than two distinct prime factors
        if p1 > p2:
            p1, p2 = p2, p1
        key = (p1 << 24) | p2
        prev = get(key)
        if prev is None or n > prev:
            max_for_pair[key] = n

    total = 0
    for v in max_for_pair.values():
        total += v
    print(total)

if __name__ == "__main__":
    main()
