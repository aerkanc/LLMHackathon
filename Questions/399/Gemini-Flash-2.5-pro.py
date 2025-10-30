import math
import multiprocessing
import sys
from functools import lru_cache

# Set higher recursion depth for the inclusion-exclusion
sys.setrecursionlimit(5000)


# --- Utility Functions ---

def gcd(a, b):
    """Compute the greatest common divisor of a and b."""
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Compute the least common multiple of a and b."""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


# --- Matrix and Fibonacci Functions ---

def mat_mult(A, B, m):
    """Multiply two 2x2 matrices modulo m."""
    C = [[0, 0], [0, 0]]
    C[0][0] = (A[0][0] * B[0][0] + A[0][1] * B[1][0]) % m
    C[0][1] = (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % m
    C[1][0] = (A[1][0] * B[0][0] + A[1][1] * B[1][0]) % m
    C[1][1] = (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % m
    return C


def mat_pow(A, n, m):
    """Compute A^n modulo m for a 2x2 matrix."""
    res = [[1, 0], [0, 1]]  # Identity matrix
    base = A
    while n > 0:
        if n % 2 == 1:
            res = mat_mult(res, base, m)
        base = mat_mult(base, base, m)
        n //= 2
    return res


def fib_mod(n, m):
    """Compute F(n) modulo m."""
    if n == 0:
        return 0
    # F(n) is T^n[0][1] where T = [[1, 1], [1, 0]]
    T = mat_pow([[1, 1], [1, 0]], n, m)
    return T[0][1]


# --- Number Theory Functions ---

@lru_cache(maxsize=None)
def prime_factors(n):
    """Get prime factors of n. Caching helps as p+1, p-1 are repeated."""
    factors = set()
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.add(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.add(temp)
    return factors


def legendre(a, p):
    """Compute the Legendre symbol (a/p)."""
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls


@lru_cache(maxsize=None)
def get_k(p):
    """Compute the rank of apparition k(p)."""
    if p == 2:
        return 3
    if p == 3:
        return 4
    if p == 5:
        return 5

    # k(p) divides n = p - (5/p)
    if legendre(5, p) == 1:
        n = p - 1
    else:
        n = p + 1

    factors = prime_factors(n)
    k = n

    # Find the smallest divisor k of n for which F(k) % p == 0
    # by checking n/q for each prime factor q
    for q in factors:
        test_k = k // q
        # Use matrix power to check F(test_k) % p
        while (fib_mod(test_k, p) == 0):
            k = test_k
            if k % q != 0:
                break
            test_k = k // q
    return k


def sieve(n):
    """Generate primes up to n using a simple sieve."""
    primes = [True] * (n + 1)
    primes[0] = primes[1] = False
    for i in range(2, int(math.sqrt(n)) + 1):
        if primes[i]:
            for multiple in range(i * i, n + 1, i):
                primes[multiple] = False
    prime_numbers = [i for i, is_prime in enumerate(primes) if is_prime]
    return prime_numbers


# --- Worker for Parallel S_min Generation ---

def generate_s_list_worker(p_batch):
    """Worker function to compute s_p = p*k(p) for a batch of primes."""
    s_list = []
    for p in p_batch:
        s_list.append(p * get_k(p))
    return s_list


# --- Inclusion-Exclusion Function ---

@lru_cache(maxsize=None)
def calc_C_recursive(N, S_min_tuple, index, current_lcm):
    """
    Recursively compute the count of "squareful" indices <= N using
    inclusion-exclusion. Pruning (if l > N) is critical.
    """
    count = 0
    for i in range(index, len(S_min_tuple)):
        s = S_min_tuple[i]

        # Avoid overflow and prune
        try:
            # Check for potential overflow before lcm
            if current_lcm > N // s:
                l = N + 1
            else:
                l = lcm(current_lcm, s)
        except:
            l = N + 1

        if l > N:
            continue

        # Add N/l (inclusion)
        term = N // l
        # Subtract C(N, S_min, i+1, l) (exclusion)
        count += term - calc_C_recursive(N, S_min_tuple, i + 1, l)

    return count


def calc_f(N, S_min_list):
    """Compute f(N) = N - C(N) (count of squarefree indices)."""
    # Convert list to tuple for lru_cache
    S_min_tuple = tuple(S_min_list)
    C_N = calc_C_recursive(N, S_min_tuple, 0, 1)
    return N - C_N


# --- Main Execution ---

def main():
    TARGET_COUNT = 100_000_000

    # We need to generate S_min. The terms s=p*k(p) grow, but the
    # inclusion-exclusion sum is dominated by the smallest terms.
    # A limit of 2,000,000 covers the most significant terms.
    # The smallest lcm of 8 terms from S_min exceeds 2e8, so the
    # recursive depth is naturally limited.
    S_MIN_LIMIT = 2_000_000

    primes = sieve(S_MIN_LIMIT)

    # 1. Generate S = {p*k(p)} in parallel
    num_cores = multiprocessing.cpu_count()
    chunk_size = (len(primes) + num_cores - 1) // num_cores
    p_batches = [primes[i:i + chunk_size] for i in range(0, len(primes), chunk_size)]

    S_all = []
    with multiprocessing.Pool(num_cores) as pool:
        results = pool.map(generate_s_list_worker, p_batches)
        for sublist in results:
            S_all.extend(sublist)

    S_all = sorted(list(set(s for s in S_all if s <= S_MIN_LIMIT)))

    # 2. Build the minimal set S_min
    S_min_set = set()
    for s_p in S_all:
        is_minimal = True
        for s in S_min_set:
            if s_p % s == 0:
                is_minimal = False
                break

        if is_minimal:
            # Remove any existing elements divisible by this new minimal s_p
            to_remove = {s for s in S_min_set if s % s_p == 0}
            S_min_set.difference_update(to_remove)
            S_min_set.add(s_p)

    S_min_list = sorted(list(S_min_set))

    # 3. Binary search for the target N
    # Estimate density: 200th squarefree num is F_~260.
    # Density approx 200/260 ~ 0.77.
    # N_approx = 100M / 0.77 ~ 130M.
    # Set search range around this estimate.
    low = TARGET_COUNT
    high = int(TARGET_COUNT / 0.75)  # Upper bound
    target_N = high

    while low <= high:
        mid = (low + high) // 2
        f_mid = calc_f(mid, S_min_list)

        if f_mid >= TARGET_COUNT:
            target_N = mid  # This is a potential answer
            high = mid - 1
        else:
            low = mid + 1

    # After loop, target_N is the smallest N s.t. f(N) >= TARGET_COUNT
    # This is the 100,000,000th squarefree index.

    # 4. Calculate final F(N) properties

    # a) Last 16 digits
    # Pisano period for 10^16 is lcm(pi(2^16), pi(5^16))
    # pi(2^16) = 3 * 2^(16-1) = 3 * 2^15
    # pi(5^16) = pi(5) * 5^(16-1) = 20 * 5^15 = 4 * 5^16
    # lcm(3 * 2^15, 4 * 5^16) = lcm(3 * 2^15, 2^2 * 5^16)
    # = 3 * 2^15 * 5^16 = 15 * 10^15
    P = 15 * (10 ** 15)
    N_mod_P = target_N % P

    T_res = mat_pow([[1, 1], [1, 0]], N_mod_P, 10 ** 16)
    last_digits = T_res[0][1]
    last_digits_str = str(last_digits).zfill(16)

    # b) Scientific notation
    # log10(F(N)) approx N*log10(phi) - 0.5*log10(5)
    LOG10_PHI = math.log10((1 + math.sqrt(5)) / 2)
    LOG10_SQRT5 = math.log10(math.sqrt(5))

    log_F_N = target_N * LOG10_PHI - LOG10_SQRT5

    exponent = math.floor(log_F_N)
    mantissa = 10 ** (log_F_N - exponent)

    sci_not = f"{mantissa:.1f}e{exponent}"

    # 5. Print the result
    print(f"{last_digits_str},{sci_not}")


if __name__ == "__main__":
    main()
