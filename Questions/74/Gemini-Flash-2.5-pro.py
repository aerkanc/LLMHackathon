import multiprocessing
import sys

# Set higher recursion depth for deep chains, although our iterative
# approach doesn't need it, it's good practice for complex problems.
sys.setrecursionlimit(2000)

# These will be read-only globals in the worker processes
SUM_CACHE = []
# Pre-calculate factorials for digits 0-9
FACTORIALS = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]  # 0! to 9!


def init_worker(cache):
    """
    Initializer for each worker process.
    This function is called once per worker when it starts.
    It sets the global SUM_CACHE to the pre-computed cache from the main process.
    """
    global SUM_CACHE
    SUM_CACHE = cache


def sum_digit_factorials(n):
    """
    Helper function to compute the sum of digit factorials.
    This is used *only* for pre-computing the cache in the main process.
    """
    global FACTORIALS
    if n == 0:
        return 1  # FACTORIALS[0]
    sum_fact = 0
    temp_n = n
    while temp_n > 0:
        sum_fact += FACTORIALS[temp_n % 10]
        temp_n //= 10
    return sum_fact


def get_chain_length(n):
    """
    Computes the length of the non-repeating chain starting from n.
    This function is executed by the worker processes.
    It relies on the global SUM_CACHE being initialized and read-only.
    """
    global SUM_CACHE
    chain_terms = set()
    current_n = n

    # Loop until we find a number already seen in this *specific* chain
    while current_n not in chain_terms:
        chain_terms.add(current_n)
        # Get the next term from the pre-computed cache.
        # This is a very fast lookup.
        current_n = SUM_CACHE[current_n]

    # The length is the number of unique terms we found.
    return len(chain_terms)


def solve():
    """
    Main function to solve the problem.
    1. Pre-computes the sum_digit_factorials for all possible numbers.
    2. Sets up a multiprocessing pool.
    3. Maps the get_chain_length function across all starting numbers.
    4. Counts the results and prints the final answer.
    """
    LIMIT = 1000000
    TARGET_LENGTH = 60

    # Determine the maximum number we will ever need to query in the cache.
    # The starting numbers are < 1,000,000.
    # The max sum for a 6-digit number is sum_digit_factorials(999,999)
    # which is 6 * 9! = 6 * 362,880 = 2,177,280.
    # Any number in any chain starting < 1M will be <= 2,177,280.
    # So, we need to cache results for numbers from 0 up to 2,177,280.
    # The size of the list needs to be one larger to include this index.
    N_MAX = 2177280 + 1

    # 1. Pre-compute the sum_digit_factorials cache in the main process.
    # This list will be passed to each worker process.
    # Using a list for O(1) index-based lookup.
    local_sum_cache = [0] * N_MAX
    for i in range(N_MAX):
        local_sum_cache[i] = sum_digit_factorials(i)

    # 2. Set up the multiprocessing pool
    # Use 16 cores as specified in the problem.
    num_cores = 16

    # chunksize helps multiprocessing be more efficient by sending
    # work in batches rather than one item at a time.
    # We'll divide the work into 16 * 16 = 256 chunks.
    chunksize = max(1, (LIMIT // (num_cores * 16)))

    with multiprocessing.Pool(processes=num_cores, initializer=init_worker, initargs=(local_sum_cache,)) as pool:
        # 3. Map the work to the pool
        # pool.map applies get_chain_length to
        # each item in range(LIMIT) and returns a list of the results.
        results = pool.map(get_chain_length, range(LIMIT), chunksize=chunksize)

    # 4. Count the results
    # list.count() is an efficient C-implemented way to count items.
    total_count = results.count(TARGET_LENGTH)

    # Print *only* the final answer to stdout.
    print(total_count)


if __name__ == "__main__":
    # This check is essential for multiprocessing to work correctly
    # on systems that spawn new processes (like Windows).
    multiprocessing.freeze_support()
    solve()
