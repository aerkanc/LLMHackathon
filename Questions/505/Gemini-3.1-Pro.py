import sys
from multiprocessing import Pool

# Increase recursion depth to safely accommodate tree depths of ~40
sys.setrecursionlimit(3000)

n = 10 ** 12
M = (1 << 60) - 1
D_base = n.bit_length() - 1

# Caching dictionary for parallel results
memo_results = {}


def get_x(k):
    """Computes x(k) in O(log k) using the matrix sequence properties."""
    if k == 0: return 0
    if k == 1: return 1
    # Binary representation ignoring the '0b' and the first leading '1'
    bin_k = bin(k)[3:]
    x1, x0 = 1, 0
    for b in bin_k:
        if b == '0':
            nx1 = (3 * x1 + 2 * x0) & M
            nx0 = x1
        else:
            nx1 = (2 * x1 + 3 * x0) & M
            nx0 = x1
        x1, x0 = nx1, nx0
    return x1


def get_max_depth(k):
    """Calculates the maximum depth of the leaves in the subtree rooted at k."""
    L = k.bit_length() - 1
    shift = D_base - L
    if shift < 0:
        return L
    # Check the left-most leaf descendant
    if (k << shift) >= n:
        return D_base
    return D_base + 1


def compute_val(k, alpha, beta):
    """Alpha-Beta / Negamax style pruning down the recurrence tree."""
    if k in memo_results:
        return memo_results[k]

    if k >= n:
        return get_x(k)

    # Invert the bounds for the max() logic to work natively
    alpha_prime = M - beta
    beta_prime = M - alpha

    depth = get_max_depth(k)
    d_k = depth - (k.bit_length() - 1)
    d_child = d_k - 1

    # Heuristic for perfect move ordering:
    # Determine MIN/MAX node properties based on the parity of the distance to the leaves
    if d_child % 2 == 0:
        c1, c2 = 2 * k, 2 * k + 1
    else:
        c1, c2 = 2 * k + 1, 2 * k

    # Search first child branch
    v1 = compute_val(c1, alpha_prime, beta_prime)
    if v1 >= beta_prime:
        return M - v1

    # Tighten bounds and search second child branch
    alpha_prime = max(alpha_prime, v1)
    v2 = compute_val(c2, alpha_prime, beta_prime)

    return M - max(v1, v2)


def worker(k):
    """Worker task wrapper for multiprocessing evaluating independent subtrees."""
    return k, compute_val(k, 0, M)


def solve():
    # To utilize all cores optimally, we split the tree execution at level 6.
    # Level 6 yields 64 independent subtrees, easily balancing load across 16+ cores.
    split_level = min(6, D_base - 1)
    if split_level < 0:
        split_level = 0

    start_k = 1 << split_level
    end_k = 2 << split_level
    tasks = list(range(start_k, end_k))

    # Parallelize the heavy subtree bounds without alpha-beta crossover blockages
    with Pool() as pool:
        res = pool.map(worker, tasks)

    memo_results.update(dict(res))

    # Calculate the remaining top layers
    ans = compute_val(1, 0, M)
    print(ans)


if __name__ == '__main__':
    solve()