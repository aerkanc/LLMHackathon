#!/usr/bin/env python3

def solve():
    """
    This script calculates the solution to Project Euler Problem 301.

    The problem asks for the number of positive integers n <= 2^30 such that
    n XOR (2*n) XOR (3*n) = 0.

    This condition is equivalent to (n XOR 2*n) = 3*n.
    The equality (a XOR b) == (a + b) holds if and only if (a AND b) == 0.
    In our case, a=n and b=2*n. Since n + 2*n = 3*n, the condition simplifies to
    (n AND (2*n)) == 0.

    In binary, n = ...b_2 b_1 b_0
    and       2*n = ...b_2 b_1 b_0 0
    The condition (n AND 2*n) == 0 means that for any bit position i,
    the i-th bit of n and the i-th bit of 2*n cannot both be 1.
    This implies that b_i AND b_{i-1} must be 0 for all i >= 1.
    In other words, n cannot have consecutive '1's in its binary representation.

    We need to count how many such numbers n exist for 1 <= n <= 2^30.
    This count can be found using the Fibonacci sequence.

    Let h(k) be the count of k-bit numbers (which start with '1') that
    have no consecutive '1's.
    h(k) = F_k (the k-th Fibonacci number, where F_1=1, F_2=1).

    The total count for n < 2^30 is the sum of h(k) for k=1 to 30:
    Sum(F_k for k=1 to 30) = F_{32} - 1.

    We must also check n = 2^30.
    n = 2^30 is '1' followed by 30 zeros (100...000).
    This number has no consecutive '1's, so it is a valid solution.

    The final total is (F_{32} - 1) + 1 = F_{32}.

    We just need to compute the 32nd Fibonacci number (using F_0=0, F_1=1).
    """

    # We need to find F_32
    target_n = 32

    # Initialize F_0 and F_1
    a, b = 0, 1

    # We loop target_n times to get from F_0 to F_n
    # A simpler way is to loop target_n - 1 times starting from F_1
    for _ in range(target_n - 1):
        a, b = b, a + b

    # After the loop, b holds F_32 (since we started with b=F_1 and looped 31 times)
    print(b)


if __name__ == "__main__":
    solve()
