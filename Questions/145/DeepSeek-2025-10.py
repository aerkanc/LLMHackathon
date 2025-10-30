# Project Euler style – Problem 172
# Count 18-digit numbers (no leading zeros) where no digit occurs more than three times.

from math import factorial

# Precompute factorials we need
fact = [factorial(i) for i in range(19)]
F17 = fact[17]

ans = 0

def dfs(idx: int, remaining: int, denom: int, a0: int):
    """
    idx: which digit we're assigning count to (0..9)
    remaining: digits left to place
    denom: product of factorials of assigned counts so far
    a0: the count chosen for digit 0 (only meaningful after idx>=1)
    """
    global ans
    if idx == 10:
        if remaining == 0:
            # number of sequences with first digit nonzero for this count vector:
            # 17! * (18 - a0) / prod(ai!)
            ans += (F17 * (18 - a0)) // denom
        return

    # maximum we can assign at this digit
    max_ai = min(3, remaining)
    if idx == 0:
        # choosing the count for digit 0
        for k in range(max_ai + 1):
            dfs(idx + 1, remaining - k, denom * fact[k], k)
    else:
        for k in range(max_ai + 1):
            dfs(idx + 1, remaining - k, denom * fact[k], a0)

dfs(0, 18, 1, 0)
print(ans)
