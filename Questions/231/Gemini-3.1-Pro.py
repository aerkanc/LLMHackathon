import math


def solve():
    n = 20000000
    k = 15000000
    m = n - k

    # Use a bytearray for a highly memory-efficient and fast Sieve of Eratosthenes
    sieve = bytearray([True]) * (n + 1)
    sieve[0] = False
    sieve[1] = False

    # Mark non-primes in the sieve
    for i in range(2, math.isqrt(n) + 1):
        if sieve[i]:
            sieve[i * i: n + 1: i] = bytearray([False]) * len(range(i * i, n + 1, i))

    total_sum = 0

    # Calculate the exponent of each prime in the binomial coefficient
    for p in range(2, n + 1):
        if sieve[p]:
            vp = 0
            power = p

            # Legendre's formula applied
            while power <= n:
                vp += (n // power) - (k // power) - (m // power)
                power *= p

            if vp > 0:
                total_sum += p * vp

    print(total_sum)


if __name__ == '__main__':
    solve()