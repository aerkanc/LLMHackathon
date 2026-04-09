import math
import bisect
from array import array

def sieve_odd(n: int) -> array:
    """
    Return an array of all primes up to n (inclusive) using an odd-only sieve.
    """
    if n < 2:
        return array('I')
    # number of odd numbers up to n: (n+1)//2
    size = (n + 1) // 2
    is_prime = bytearray(b'\x01') * size
    is_prime[0] = 0                     # 1 is not prime
    limit = math.isqrt(n)
    # sieve odd primes only
    for i in range(3, limit + 1, 2):
        idx = i // 2
        if is_prime[idx]:
            start = i * i
            start_idx = start // 2
            step = i
            # number of elements in the slice [start_idx :: step]
            length = (size - start_idx + step - 1) // step
            is_prime[start_idx::step] = b'\x00' * length
    # collect primes: 2 and all odd primes
    primes = array('I', [2])
    primes.extend(2 * idx + 1 for idx, flag in enumerate(is_prime) if flag)
    return primes

def count_semiprimes(N: int) -> int:
    """
    Return the number of composite integers n < N that have exactly two
    (not necessarily distinct) prime factors.
    """
    limit = N // 2                     # we need primes up to N/2
    primes = sieve_odd(limit)
    sqrtN = math.isqrt(N)
    total = 0
    for p in primes:
        if p > sqrtN:
            break
        max_q = (N - 1) // p           # largest q such that p*q < N
        lo = bisect.bisect_left(primes, p)
        hi = bisect.bisect_right(primes, max_q) - 1
        if hi >= lo:
            total += (hi - lo + 1)
    return total

if __name__ == "__main__":
    N = 10 ** 8
    result = count_semiprimes(N)
    print(result)