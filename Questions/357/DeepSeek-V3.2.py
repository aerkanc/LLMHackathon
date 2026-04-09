import math
import multiprocessing

LIMIT = 100_000_000

# Global data (shared read-only among processes)
is_prime = None          # bytearray of primality up to LIMIT+1
odd_primes = None        # list of odd primes <= 10000


def sieve(limit: int) -> bytearray:
    """Return a bytearray is_prime[0..limit] with is_prime[i]=1 iff i is prime."""
    is_prime = bytearray(b'\x01') * (limit + 1)
    is_prime[0:2] = b'\x00\x00'
    sqrt = int(limit ** 0.5)
    for i in range(2, sqrt + 1):
        if is_prime[i]:
            start = i * i
            step = i
            is_prime[start:limit+1:step] = b'\x00' * ((limit - start) // step + 1)
    return is_prime


def get_prime_factors(n: int):
    """
    Return a list of distinct prime factors of n if n is squarefree,
    otherwise return None.
    """
    factors = []
    # factor 2
    if n % 2 == 0:
        factors.append(2)
        n //= 2
        if n % 2 == 0:          # square factor 2
            return None
        if n == 1:
            return factors
        if is_prime[n]:         # remaining part is prime
            factors.append(n)
            return factors

    # n is now odd and >1
    for p in odd_primes:
        if p * p > n:
            break
        if n % p == 0:
            factors.append(p)
            n //= p
            if n % p == 0:      # square factor p
                return None
            if is_prime[n]:     # remaining part is prime
                factors.append(n)
                return factors
    if n > 1:                   # n is prime (and > sqrt(original n))
        factors.append(n)
    return factors


def check_condition(n: int, factors):
    """Return True if for every divisor d of n, d + n/d is prime."""
    # generate all divisors (n is squarefree, factors are distinct)
    divisors = [1]
    for p in factors:
        divisors += [d * p for d in divisors]
    for d in divisors:
        if not is_prime[d + n // d]:
            return False
    return True


def process_chunk(chunk):
    """Process a range of even numbers [start, end] (step 2)."""
    start, end = chunk
    total = 0
    for n in range(start, end + 1, 2):
        # n must be squarefree, so not divisible by 4
        if n % 4 == 0:
            continue
        # n+1 must be prime (necessary condition)
        if is_prime[n + 1]:
            factors = get_prime_factors(n)
            if factors is not None and check_condition(n, factors):
                total += n
    return total


def main():
    global is_prime, odd_primes

    # Precompute primality up to LIMIT+1 (max possible d+n/d)
    is_prime = sieve(LIMIT + 1)

    # Precompute odd primes up to 10000 (sqrt(LIMIT))
    small_primes = [i for i in range(2, 10001) if is_prime[i]]
    odd_primes = small_primes[1:]      # skip 2

    # n = 1 always qualifies
    total_sum = 1

    # Split even numbers 2,4,6,...,LIMIT into chunks for parallel processing
    num_workers = multiprocessing.cpu_count()
    total_evens = LIMIT // 2
    chunk_size = total_evens // num_workers
    chunks = []
    for i in range(num_workers):
        start = 2 + 2 * i * chunk_size
        end = start + 2 * chunk_size - 2
        if i == num_workers - 1:
            end = LIMIT
        chunks.append((start, end))

    with multiprocessing.Pool(num_workers) as pool:
        results = pool.map(process_chunk, chunks)

    total_sum += sum(results)
    print(total_sum)


if __name__ == "__main__":
    main()