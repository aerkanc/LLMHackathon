def sieve(n):
    """Generate all primes up to n using Sieve of Eratosthenes"""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]


def find_max_product(p, q, N):
    """Find largest p^a * q^b <= N where a, b >= 1"""
    max_val = 0
    pa = p
    while pa <= N:
        # For this power of p, find the largest power of q such that pa * qb <= N
        limit = N // pa
        # Only proceed if at least q^1 fits (ensure both p and q are factors)
        if q <= limit:
            qb = q
            while qb * q <= limit:
                qb *= q
            max_val = max(max_val, pa * qb)
        pa *= p
    return max_val


def S(N):
    """Compute sum of all distinct M(p, q, N) for prime pairs (p, q)"""
    primes = sieve(N)
    total = 0

    # Iterate through all pairs of distinct primes
    for i in range(len(primes) - 1):
        p = primes[i]

        for j in range(i + 1, len(primes)):
            q = primes[j]
            # Only valid pairs have p*q <= N
            if p * q > N:
                break

            m = find_max_product(p, q, N)
            total += m

    return total


print(S(10000000))