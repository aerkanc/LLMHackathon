import numpy as np
import multiprocessing
import os

# --- Globals for Worker Processes ---
# These will be initialized in each worker process to avoid passing
# large objects repeatedly.
worker_primes = None
worker_N = 0


def sieve_of_eratosthenes(limit):
    """
    Generates primes up to a given limit using a NumPy-based sieve.
    """
    # Create a boolean array "is_prime"
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[0:2] = False  # 0 and 1 are not prime

    # Perform the sieve
    for p in range(2, int(np.sqrt(limit)) + 1):
        if is_prime[p]:
            # Mark all multiples of p as not prime
            is_prime[p * p::p] = False

    # Return the indices where is_prime is True
    return np.where(is_prime)[0]


def calculate_M(p, q, N):
    """
    Calculates M(p, q, N), the largest integer <= N divisible by
    only primes p and q (and by both).
    """
    max_m = 0
    pow_p = p

    # Iterate through powers of p: p^a
    while pow_p <= N / q:  # Ensures p^a * q^1 is at most N
        pow_q = q
        # Iterate through powers of q: q^b
        while True:
            current_m = pow_p * pow_q
            if current_m > N:
                break

            max_m = max(max_m, current_m)

            # Check for potential overflow before multiplication
            if pow_q > N // q:
                break
            pow_q *= q

        # Check for potential overflow before multiplication
        if pow_p > N // p:
            break
        pow_p *= p

    return max_m


def init_worker(primes_arg, N_arg):
    """
    Initializer function for each worker in the multiprocessing pool.
    Sets global variables for the worker's lifetime.
    """
    global worker_primes, worker_N
    worker_primes = primes_arg
    worker_N = N_arg


def compute_m_for_p(i):
    """
    A single task to be run by a worker process.
    Calculates all M(p, q, N) for a given prime p (at index i).
    """
    global worker_primes, worker_N

    p = worker_primes[i]
    local_m_values = set()
    n_primes = len(worker_primes)

    # Iterate through all q > p
    for j in range(i + 1, n_primes):
        q = worker_primes[j]

        # Optimization: If p*q > N, then no M exists for this
        # p and any subsequent q.
        if p * q > worker_N:
            break

        m_val = calculate_M(p, q, worker_N)
        if m_val > 0:
            local_m_values.add(m_val)

    return local_m_values


def solve_problem():
    """
    Main function to orchestrate the prime generation,
    parallel computation, and final summation.
    """
    N = 10_000_000

    # 1. Generate all primes up to N/2.
    # We only need q <= N/2 (since p=2 is the smallest p).
    primes = sieve_of_eratosthenes(N // 2)

    n_primes = len(primes)

    # 2. Determine the range of 'p' primes to process.
    # We only need to iterate p up to sqrt(N), because
    # if p > sqrt(N), then q > p > sqrt(N),
    # which means p*q > N, so M(p,q,N) would be 0.
    i_limit = n_primes
    for i in range(n_primes):
        p = primes[i]
        if p * p > N:
            i_limit = i
            break

    # The indices of p we need to process
    indices_to_process = range(i_limit)

    global_m_values = set()

    # 3. Set up and run the multiprocessing pool
    try:
        # Use all available cores
        num_cores = os.cpu_count() or 16
    except NotImplementedError:
        num_cores = 16  # Fallback

    with multiprocessing.Pool(processes=num_cores,
                              initializer=init_worker,
                              initargs=(primes, N)) as pool:

        # imap_unordered is efficient for jobs of uneven size.
        # chunksize=1 ensures the larger tasks (for small p)
        # are picked up quickly and don't block smaller ones.
        results_iterator = pool.imap_unordered(compute_m_for_p,
                                               indices_to_process,
                                               chunksize=1)

        # 4. Collect results as they complete
        for local_set in results_iterator:
            global_m_values.update(local_set)

    # 5. Calculate final sum. The set automatically handled 0s
    # (if they were added) and duplicates.
    if 0 in global_m_values:
        global_m_values.remove(0)

    total_sum = sum(global_m_values)

    # 6. Print ONLY the final answer
    print(total_sum)


if __name__ == "__main__":
    solve_problem()
