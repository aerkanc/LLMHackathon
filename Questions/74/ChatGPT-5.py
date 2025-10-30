# Project Euler Problem 74 – Digit factorial chains
# Count starting numbers below one million that produce chains with exactly 60 non-repeating terms.

import math
from functools import lru_cache

# Precompute factorials of digits 0..9
FACT = [math.factorial(i) for i in range(10)]

# Max value any term can reach for starts < 1_000_000:
# 6*9! = 2177280; after that, the maximum is bounded by 7*9! = 2540160
MAX_VAL = 7 * FACT[9]
CACHE_SIZE = MAX_VAL + 1

# Cache for chain lengths; 0 means unknown (lengths are >=1 when known)
cache = [0] * CACHE_SIZE

def digit_fact_sum(n: int) -> int:
    s = 0
    while n:
        n, d = divmod(n, 10)
        s += FACT[d]
    return s or FACT[0]  # handle n == 0

def chain_length(start: int) -> int:
    seen_index = {}
    seq = []

    n = start
    while True:
        # If we already computed length from this n, use it
        if n < CACHE_SIZE and cache[n]:
            known_len = cache[n]
            total_len = len(seq) + known_len
            # propagate lengths back through the sequence
            for i, val in enumerate(seq):
                l = total_len - i
                if val < CACHE_SIZE and cache[val] == 0:
                    cache[val] = l
            return total_len

        # If we loop within the current sequence
        if n in seen_index:
            loop_start = seen_index[n]
            loop_len = len(seq) - loop_start
            # assign lengths for nodes in the sequence
            for i, val in enumerate(seq):
                if val < CACHE_SIZE and cache[val] == 0:
                    if i < loop_start:
                        cache[val] = len(seq) - i
                    else:
                        cache[val] = loop_len
            return len(seq)

        # Continue building the chain
        seen_index[n] = len(seq)
        seq.append(n)
        n = digit_fact_sum(n)

def main():
    limit = 1_000_000
    target_len = 60
    count = 0
    for n in range(1, limit):
        if chain_length(n) == target_len:
            count += 1
    print(count)

if __name__ == "__main__":
    main()
