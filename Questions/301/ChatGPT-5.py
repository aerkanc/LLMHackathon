# Project Euler-style problem (Nim): count positive integers n <= 2^30
# such that n ^ (2n) ^ (3n) == 0. This holds iff n has no consecutive 1s in binary.
# So we count numbers in (0, 2^30] without consecutive ones.

def count_no_consecutive_ones_upto(N: int) -> int:
    # DP with Fibonacci-like counts per bit length
    # fib[i]: number of binary strings of length i without consecutive ones
    fib = [0] * 64
    fib[0], fib[1] = 1, 2  # "" and "0"/"1"
    for i in range(2, 64):
        fib[i] = fib[i-1] + fib[i-2]

    res = 0
    prev_one = 0
    # traverse bits from high to low
    for i in reversed(range(N.bit_length())):
        if (N >> i) & 1:
            res += fib[i]          # place 0 here, remaining i bits free
            if prev_one:           # found consecutive ones -> stop (exclude N itself)
                return res
            prev_one = 1
        else:
            prev_one = 0
    return res + 1  # include N itself if it doesn't contain "11"

N = 1 << 30
# exclude 0 to keep only positive integers
answer = count_no_consecutive_ones_upto(N) - 1
print(answer)
