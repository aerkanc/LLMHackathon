import numpy as np
from multiprocessing import Pool
import os


def calculate_floor_pm(m):
    """
    Calculates the integer part of the maximised product P_m for a given m.

    This function uses numpy.longdouble for extended precision, which is
    necessary to get the correct floor value for values like P_10.
    """

    # Cast m to longdouble for precision
    m_ld = np.longdouble(m)
    two_ld = np.longdouble(2)

    # Create an array k = [1, 2, ..., m]
    k_array = np.arange(1, m + 1, dtype=np.longdouble)

    # Calculate sum_{k=1 to m} k * ln(k)
    sum_k_log_k = np.sum(k_array * np.log(k_array))

    # Calculate the exponent term: m*(m+1)/2
    exponent = m_ld * (m_ld + 1) / two_ld

    # Calculate ln(P_m) using the formula:
    # ln(P_m) = [m(m+1)/2] * (ln(2) - ln(m+1)) + sum(k*ln(k))
    log_term1 = exponent * (np.log(two_ld) - np.log(m_ld + 1))
    log_pm = log_term1 + sum_k_log_k

    # Exponentiate to get P_m
    pm = np.exp(log_pm)

    # Return the integer part (floor) of P_m.
    # We cast to a standard python int so it can be easily summed.
    return int(np.floor(pm))


def solve():
    """
    Calculates the sum of floor(P_m) for m from 2 to 15 using a
    multiprocessing pool.
    """

    # The range of m values to compute
    m_values = list(range(2, 16))

    # Determine the number of cores to use
    # We leave one core free for system tasks, or use 1 if only 1 is available
    try:
        num_cores = max(1, os.cpu_count() - 1)
    except (NotImplementedError, AttributeError):
        num_cores = 4  # Fallback

    # Use a multiprocessing Pool to compute the values in parallel
    # The 'spawn' start method is more compatible across platforms
    import multiprocessing
    ctx = multiprocessing.get_context('spawn')

    with ctx.Pool(processes=num_cores) as pool:
        # pool.map applies the function to each item in m_values
        # and returns a list of the results in order.
        results = pool.map(calculate_floor_pm, m_values)

    # The results are a list of integers [floor(P_2), floor(P_3), ..., floor(P_15)]
    # Sum them to get the final answer.
    total_sum = sum(results)

    # Print only the final result
    print(total_sum)


if __name__ == "__main__":
    # The __name__ == "__main__" block is required for
    # multiprocessing to work correctly on all platforms.
    solve()
