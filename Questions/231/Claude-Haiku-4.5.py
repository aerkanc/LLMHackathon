import multiprocessing as mp
from functools import partial


def sieve_of_eratosthenes(limit):
    """Generate all primes up to limit using Sieve of Eratosthenes"""
    if limit < 2:
        return []

    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

    return [i for i in range(2, limit + 1) if is_prime[i]]


def exponent_in_factorial(n, p):
    """Calculate exponent of prime p in n! using Legendre's formula"""
    exp = 0
    pk = p
    while pk <= n:
        exp += n // pk
        pk *= p
    return exp


def compute_small_prime_contribution(p, n, k, m):
    """Compute contribution of a small prime p to the sum"""
    exp_n = exponent_in_factorial(n, p)
    exp_k = exponent_in_factorial(k, p)
    exp_m = exponent_in_factorial(m, p)
    exp = exp_n - exp_k - exp_m
    return p * exp


def solve():
    n = 20000000
    k = 15000000
    m = n - k  # 5000000

    # Generate all primes up to n
    primes = sieve_of_eratosthenes(n)

    # Separate primes into two groups
    small_primes = [p for p in primes if p <= m]
    large_primes = [p for p in primes if k < p <= n]

    # Part 1: Compute contribution from small primes using multiprocessing
    compute_func = partial(compute_small_prime_contribution, n=n, k=k, m=m)

    with mp.Pool() as pool:
        results = pool.map(compute_func, small_primes, chunksize=1000)

    sum_small = sum(results)

    # Part 2: Large primes (in range (k, n]) each contribute exactly themselves (exponent = 1)
    sum_large = sum(large_primes)

    total_sum = sum_small + sum_large
    print(total_sum)


if __name__ == '__main__':
    solve()