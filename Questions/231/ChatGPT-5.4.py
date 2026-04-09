N = 20_000_000
K = 15_000_000
R = N - K  # 5_000_000


def odd_prime_sieve(n: int) -> bytearray:
    sieve = bytearray(b"\x01") * (n // 2 + 1)
    sieve[0] = 0  # 1 is not prime
    limit = int(n ** 0.5)
    for p in range(3, limit + 1, 2):
        if sieve[p // 2]:
            start = p * p
            idx = start // 2
            sieve[idx::p] = b"\x00" * len(sieve[idx::p])
    return sieve


def vp_binom(p: int, n: int, k: int, r: int) -> int:
    e = 0
    q = p
    while q <= n:
        e += n // q - k // q - r // q
        q *= p
    return e


sieve = odd_prime_sieve(N)

total = 0

# prime 2
total += 2 * vp_binom(2, N, K, R)

# odd primes
for p in range(3, N + 1, 2):
    if sieve[p // 2]:
        total += p * vp_binom(p, N, K, R)

print(total)