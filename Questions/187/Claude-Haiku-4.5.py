def sieve_of_eratosthenes(n):
    """Generate all primes up to n"""
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    return [i for i in range(2, n + 1) if is_prime[i]]


def count_primes_in_range(low, high, small_primes):
    """Count primes in [low, high] using segmented sieve"""
    if low > high or high < 2:
        return 0

    low = max(low, 2)

    length = high - low + 1
    is_prime = [True] * length

    # Mark composites using small primes
    for p in small_primes:
        if p * p > high:
            break

        # Find first multiple of p >= low (but not p itself if in range)
        start = max(p * p, ((low + p - 1) // p) * p)

        # Mark all multiples of p as composite
        for j in range(start, high + 1, p):
            is_prime[j - low] = False

    return sum(is_prime)


def count_semiprimes(limit):
    sqrt_limit = int(limit ** 0.5)
    small_primes = sieve_of_eratosthenes(sqrt_limit)

    count = 0

    # Count p^2 semiprimes (p is prime, p^2 < limit)
    for p in small_primes:
        if p * p >= limit:
            break
        count += 1

    # Count p*q semiprimes where p < q (both prime, p*q < limit)
    # For each small prime p, count primes q where p < q < limit/p
    for p in small_primes:
        max_q = (limit - 1) // p

        if max_q <= p:
            # No valid q > p exists
            break

        # Count primes in range (p, max_q]
        count += count_primes_in_range(p + 1, max_q, small_primes)

    return count


limit = 10 ** 8
result = count_semiprimes(limit)
print(result)