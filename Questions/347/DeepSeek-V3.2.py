import multiprocessing as mp
from bisect import bisect_right
import math

N = 10_000_000

# Global data for worker processes (shared via copy-on-write)
primes_global = None
powers_global = None
N_global = None

def sieve(limit: int):
    """Return list of all primes up to limit."""
    is_prime = bytearray(b'\x01') * (limit + 1)
    is_prime[0:2] = b'\x00\x00'
    sqrt = int(math.isqrt(limit))
    for i in range(2, sqrt + 1):
        if is_prime[i]:
            start = i * i
            step = i
            is_prime[start:limit+1:step] = b'\x00' * ((limit - start) // step + 1)
    return [i for i, v in enumerate(is_prime) if v]

def compute_powers(primes, limit):
    """For each prime p, precompute p^1, p^2, ... ≤ limit."""
    powers = []
    for p in primes:
        lst = [p]
        while lst[-1] * p <= limit:
            lst.append(lst[-1] * p)
        powers.append(lst)
    return powers

def worker(p_idx):
    """Compute sum of M(p,q,N) for a fixed p (by index)."""
    p = primes_global[p_idx]
    powers_p = powers_global[p_idx]
    total = 0
    # q must be > p and p*q ≤ N
    for j in range(p_idx + 1, len(primes_global)):
        q = primes_global[j]
        if p * q > N_global:
            break
        powers_q = powers_global[j]
        best = 0
        for pa in powers_p:
            target = N_global // pa
            idx = bisect_right(powers_q, target)
            if idx == 0:
                continue
            candidate = pa * powers_q[idx - 1]
            if candidate > best:
                best = candidate
        total += best
    return total

def main():
    global primes_global, powers_global, N_global
    N_global = N

    # Generate primes up to N
    primes = sieve(N)
    primes_global = primes

    # Precompute powers for every prime
    powers = compute_powers(primes, N)
    powers_global = powers

    # Only primes p with p ≤ sqrt(N) can have a partner q > p with p*q ≤ N
    sqrtN = int(math.isqrt(N))
    p_indices = [i for i, p in enumerate(primes) if p <= sqrtN]

    # Parallel processing across all suitable p
    with mp.Pool() as pool:
        results = pool.map(worker, p_indices)

    total = sum(results)
    print(total)

if __name__ == "__main__":
    main()