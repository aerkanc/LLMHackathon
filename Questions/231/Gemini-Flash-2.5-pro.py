import numpy
import sys


# Set higher recursion depth for the linear sieve, although it's not
# strictly recursive, the chain of dependencies can be long.
# This is generally not needed for iterative solutions but good to be aware of.
# sys.setrecursionlimit(20_000_000 + 10) # Not needed for this iterative sieve

def solve():
    """
    Solves Project Euler Problem 231.

    The problem asks for the sum of the terms in the prime factorisation of
    C(n, k) = n! / (k! * (n-k)!).
    Let n = 20,000,000 and k = 15,000,000. Then m = n-k = 5,000,000.

    Let S(x) be the sum of terms in the prime factorisation of x.
    S(a*b) = S(a) + S(b).
    S(a/b) = S(a) - S(b).

    We need S(C(n, k)) = S(n!) - S(k!) - S(m!).

    Let spf(j) be the sum of prime factors of j with multiplicity.
    Example: spf(120) = spf(2^3 * 3 * 5) = 2+2+2+3+5 = 14.

    The key insight is that S(x!) = sum(spf(j) for j in 2..x).

    So, we need:
    sum(spf(j) for j in 2..n) - sum(spf(j) for j in 2..k) - sum(spf(j) for j in 2..m)

    This simplifies to:
    sum(spf(j) for j in k+1..n) - sum(spf(j) for j in 2..m)

    We can compute spf(j) for all j <= n using a linear sieve.
    """

    n = 20_000_000
    k = 15_000_000
    m = 5_000_000

    # min_prime[i] will store the smallest prime factor of i.
    # We can use int32 as the max prime factor is 20M, which fits.
    min_prime = numpy.zeros(n + 1, dtype=numpy.int32)

    # spf_sum[i] will store the sum of prime factors of i (spf(i)).
    # The max value will be for a prime p <= n, so spf_sum[p] = p.
    # max p is < 20M, so int32 is sufficient.
    spf_sum = numpy.zeros(n + 1, dtype=numpy.int32)

    # list to store primes found
    primes = []

    # Start sieve from 2 up to n
    for i in range(2, n + 1):
        if min_prime[i] == 0:
            # i is a prime number
            min_prime[i] = i
            spf_sum[i] = i
            primes.append(i)

        # This inner loop processes multiples of primes.
        # It's what makes the sieve O(n).
        # We populate the min_prime and spf_sum for composite numbers.
        for p in primes:
            j = i * p
            if j > n:
                # This multiple is out of bounds
                break

            # p is the smallest prime factor of j
            min_prime[j] = p

            # spf(j) = spf(i * p) = spf(i) + p
            spf_sum[j] = spf_sum[i] + p

            if i % p == 0:
                # If i is a multiple of p, p is the smallest
                # prime factor of i. Any further primes p' > p
                # will result in j' = i * p' where min_prime(j') is p,
                # not p'. We'll process j' when we get to i' = i * p' / p.
                # This break is the key to the O(n) complexity.
                break

    # Now the spf_sum array is fully populated.
    # We can compute the two required sums.
    # We must use int64 for the summation, as the sum
    # will be large (on the order of 10^13).
    # numpy.sum() will promote to int64 by default when summing int32,
    # but explicitly setting dtype is safer.

    # Calculate: sum(spf(j) for j in k+1..n)
    sum1 = numpy.sum(spf_sum[k + 1: n + 1], dtype=numpy.int64)

    # Calculate: sum(spf(j) for j in 2..m)
    sum2 = numpy.sum(spf_sum[2: m + 1], dtype=numpy.int64)

    # The final result
    result = sum1 - sum2

    # Print only the final result
    print(result)


if __name__ == "__main__":
    solve()
