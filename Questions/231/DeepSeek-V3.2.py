import math

def main() -> None:
    n = 20_000_000
    k = 5_000_000          # because C(20M,15M) = C(20M,5M)
    m = n - k              # 15_000_000

    # ---------- sieve of Eratosthenes ----------
    is_prime = bytearray(b'\x01') * (n + 1)
    is_prime[0:2] = b'\x00\x00'
    limit = math.isqrt(n)
    for i in range(2, limit + 1):
        if is_prime[i]:
            start = i * i
            step = i
            # mark multiples as composite using a slice assignment
            is_prime[start:n+1:step] = b'\x00' * ((n - start) // step + 1)

    # ---------- compute the required sum ----------
    total = 0
    for p in range(2, n + 1):
        if is_prime[p]:
            exp = 0
            power = p
            while power <= n:
                exp += n // power - k // power - m // power
                power *= p
            total += p * exp

    print(total)


if __name__ == "__main__":
    main()