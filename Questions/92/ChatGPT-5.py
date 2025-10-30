# Project Euler 92 — Square Digit Chains (count < 10,000,000 that end at 89)
# Uses combinatorics over digit-counts (multiset permutations) to avoid iterating all numbers.

from math import factorial

DIGITS = list(range(10))
SQR = [d*d for d in DIGITS]
MAX_SUM = 7 * 81  # maximum sum of squares for 7 digits (0..9)

# Memoization for chain endpoints over possible sums [0..567]
memo = {1: 1, 89: 89}
def chain_end(n: int) -> int:
    path = []
    while n not in memo:
        path.append(n)
        s = 0
        while n:
            n, r = divmod(n, 10)
            s += r*r
        n = s
    end = memo[n]
    for v in path:
        memo[v] = end
    return end

# Precompute for all possible sums (optional but tiny and speeds up)
for s in range(MAX_SUM + 1):
    chain_end(s)

# Multinomial coefficient for 7 digits with counts c[0..9]: 7! / Π c[i]!
FACT = [factorial(i) for i in range(8)]

def multinomial(counts):
    denom = 1
    for c in counts:
        denom *= FACT[c]
    return FACT[7] // denom

# Generate all nonnegative integer vectors (c0..c9) summing to 7
total = 0

def gen_counts(idx, remaining, counts, current_sum_sq):
    global total
    if idx == 9:
        counts[idx] = remaining
        sum_sq = current_sum_sq + remaining * SQR[idx]
        if counts[0] == 7:  # this is 0000000 -> number 0; exclude
            return
        if memo[sum_sq] == 89:
            total += multinomial(counts)
        return
    for c in range(remaining + 1):
        counts[idx] = c
        gen_counts(idx + 1, remaining - c, counts, current_sum_sq + c * SQR[idx])

gen_counts(0, 7, [0]*10, 0)

print(total)
