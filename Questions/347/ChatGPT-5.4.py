from bisect import bisect_right

N = 10_000_000

def prime_list(n):
    if n < 2:
        return []
    sieve = bytearray(b"\x01") * (n // 2 + 1)
    limit = int(n ** 0.5)
    for p in range(3, limit + 1, 2):
        if sieve[p // 2]:
            start = (p * p) // 2
            sieve[start::p] = b"\x00" * (((n // 2 - start) // p) + 1)
    return [2] + [2 * i + 1 for i in range(1, n // 2 + 1) if sieve[i] and (2 * i + 1) <= n]

def solve(n):
    primes = prime_list(n // 2)
    total = 0

    for i, p in enumerate(primes[:-1]):
        if p * primes[i + 1] > n:
            break

        p_pows = [p]
        while p_pows[-1] <= n // p:
            p_pows.append(p_pows[-1] * p)

        upper = bisect_right(primes, n // p)

        for q in primes[i + 1:upper]:
            best = 0
            qb = q

            while qb <= n // p:
                limit = n // qb
                pa = p_pows[bisect_right(p_pows, limit) - 1]
                v = pa * qb
                if v > best:
                    best = v

                if qb > n // q:
                    break
                qb *= q

            total += best

    return total

print(solve(N))