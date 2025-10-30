import math
import numpy as np
from multiprocessing import Pool, cpu_count


def matrix_power_mod(matrix, power, mod):
    """Compute matrix^power mod mod using exponentiation by squaring"""
    result = np.eye(2, dtype=np.uint64)
    base = matrix.copy()
    while power > 0:
        if power & 1:
            result = (result @ base) % mod
        base = (base @ base) % mod
        power >>= 1
    return result


def fibonacci_mod(n, mod):
    """Compute F_n mod mod using matrix exponentiation"""
    if n <= 1:
        return n % mod
    base_matrix = np.array([[1, 1], [1, 0]], dtype=np.uint64)
    powered_matrix = matrix_power_mod(base_matrix, n - 1, mod)
    return powered_matrix[0, 0] % mod


def is_quadratic_residue(n, p):
    """Check if n is a quadratic residue mod p using Euler's criterion"""
    return pow(n, (p - 1) // 2, p) == 1


def find_pisano_period_square(p):
    """Find the Pisano period for p^2"""
    if p == 2:
        return 6
    if p == 5:
        return 20

    # For odd primes, the period divides p * (p - 1) or p * (p + 1)
    # depending on whether 5 is a quadratic residue mod p
    if is_quadratic_residue(5, p):
        period_candidate = p - 1
    else:
        period_candidate = p + 1

    # The actual period for p^2 divides p * period_candidate
    for d in [1, p]:
        candidate = period_candidate * d
        if fibonacci_mod(candidate, p * p) == 0:
            if fibonacci_mod(candidate + 1, p * p) == 1:
                return candidate
    return period_candidate * p


def find_zero_positions(period, p):
    """Find all positions in the period where Fibonacci is divisible by p^2"""
    positions = []
    for i in range(period):
        if fibonacci_mod(i, p * p) == 0:
            positions.append(i)
    return positions


def process_prime(args):
    """Process a single prime to find indices where F_n is divisible by p^2"""
    p, max_n = args
    try:
        period = find_pisano_period_square(p)
        zero_positions = find_zero_positions(period, p)

        # Return all indices n <= max_n where F_n is divisible by p^2
        bad_indices = []
        for pos in zero_positions:
            n = pos
            while n <= max_n:
                bad_indices.append(n)
                n += period
        return bad_indices
    except:
        return []


def find_squarefree_indices_parallel(max_n, prime_limit=None):
    """Find all indices <= max_n that are squarefree using parallel processing"""
    if prime_limit is None:
        prime_limit = int(math.sqrt(max_n)) * 10

    # Generate primes using sieve
    sieve = np.ones(prime_limit + 1, dtype=bool)
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.sqrt(prime_limit)) + 1):
        if sieve[i]:
            sieve[i * i:prime_limit + 1:i] = False
    primes = np.where(sieve)[0].tolist()

    print(f"Checking {len(primes)} primes up to {prime_limit} for n <= {max_n}")

    # Use parallel processing to find bad indices
    with Pool(cpu_count()) as pool:
        args = [(p, max_n) for p in primes if p * p <= max_n * 10]
        results = pool.map(process_prime, args)

    # Combine all bad indices
    all_bad_indices = set()
    for bad_indices in results:
        all_bad_indices.update(bad_indices)

    # All indices from 1 to max_n are initially considered squarefree
    # Remove those that are divisible by p^2 for some prime p
    squarefree_mask = np.ones(max_n + 1, dtype=bool)
    squarefree_mask[0] = False  # F_0 = 0, not considered

    for idx in all_bad_indices:
        if idx <= max_n:
            squarefree_mask[idx] = False

    return np.where(squarefree_mask)[0]


def find_nth_squarefree_fibonacci(n):
    """Find the nth squarefree Fibonacci number using binary search"""
    # Estimate bounds based on known density
    lower_bound = n * 2
    upper_bound = n * 10

    while True:
        mid = (lower_bound + upper_bound) // 2
        squarefree_indices = find_squarefree_indices_parallel(mid)
        count = len(squarefree_indices)

        print(f"n <= {mid}: found {count} squarefree Fibonacci numbers")

        if count < n:
            lower_bound = mid + 1
        else:
            upper_bound = mid

        if count >= n and (mid == lower_bound or len(find_squarefree_indices_parallel(mid - 1)) < n):
            return squarefree_indices[n - 1]


def last_16_digits_fibonacci(n):
    """Compute last 16 digits of F_n"""
    mod = 10 ** 16
    return fibonacci_mod(n, mod)


def fibonacci_scientific_notation(n):
    """Compute scientific notation of F_n using closed-form formula"""
    # F_n ≈ φ^n / √5 where φ = (1 + √5)/2
    phi = (1 + math.sqrt(5)) / 2
    log10_fib = n * math.log10(phi) - math.log10(math.sqrt(5))

    exponent = int(log10_fib)
    mantissa = 10 ** (log10_fib - exponent)

    # Round to one digit after decimal
    mantissa_rounded = round(mantissa, 1)

    # Handle case where rounding makes mantissa 10.0
    if mantissa_rounded >= 10.0:
        mantissa_rounded /= 10.0
        exponent += 1

    return f"{mantissa_rounded}e{exponent}"


def main():
    # For the actual problem, we need the 100,000,000th squarefree Fibonacci number
    # But for testing, let's use a smaller value to verify the approach
    target_n = 100000000

    print(f"Finding the {target_n}th squarefree Fibonacci number...")

    # Find the index of the target_n-th squarefree Fibonacci number
    index = find_nth_squarefree_fibonacci(target_n)
    print(f"Index of {target_n}th squarefree Fibonacci number: {index}")

    # Compute last 16 digits
    last_16 = last_16_digits_fibonacci(index)
    last_16_str = str(last_16).zfill(16)

    # Compute scientific notation
    sci_notation = fibonacci_scientific_notation(index)

    # Print final answer
    print(f"{last_16_str},{sci_notation}")


if __name__ == "__main__":
    main()