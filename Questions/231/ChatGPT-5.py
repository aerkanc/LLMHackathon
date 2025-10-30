# Project Euler style – Problem 231
# Sum of the terms in the prime factorisation of C(20_000_000, 15_000_000)

def primes_upto(n: int):
    """Sieve of Eratosthenes returning a list of primes <= n."""
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    m = int(n ** 0.5)
    for i in range(3, m + 1, 2):
        if sieve[i]:
            step = i << 1
            start = i * i
            sieve[start:n + 1:step] = b"\x00" * (((n - start) // step) + 1)
    primes = [2]
    primes.extend(i for i in range(3, n + 1, 2) if sieve[i])
    return primes

def v_p_factorial(n: int, p: int) -> int:
    """Exponent of prime p in n! using Legendre's formula."""
    e = 0
    while n:
        n //= p
        e += n
    return e

def main():
    n = 20_000_000
    k = 15_000_000
    r = n - k  # 5_000_000

    total = 0
    for p in primes_upto(n):
        e = v_p_factorial(n, p) - v_p_factorial(k, p) - v_p_factorial(r, p)
        if e:
            total += p * e
    print(total)

if __name__ == "__main__":
    main()
