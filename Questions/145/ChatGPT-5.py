# Project Euler-style: Reversible Numbers (Problem 145)
# Count n < 10^9 such that n + reverse(n) has only odd digits
# (No leading zeros in n or reverse(n))

from functools import lru_cache

def pair_generator(constrained):
    """Yield digit pairs (a,b) for the current outermost column.
       If constrained=True, forbid zeros on both outer digits (first/last digit of n)."""
    if constrained:
        a_range = range(1, 10)
        b_range = range(1, 10)
    else:
        a_range = range(10)
        b_range = range(10)
    for a in a_range:
        for b in b_range:
            yield a, b

@lru_cache(maxsize=None)
def count_ways(length, carry_in, constrained_outer):
    """
    Return (count_to_carry0, count_to_carry1) for filling a number segment
    of 'length' columns (from least-significant inward) given incoming carry.
    - For length >= 2: choose outer digit pair (a,b), ensure both occurrences
      (rightmost and its mirrored leftmost) yield odd digits, and recurse into
      the inner segment (length-2) with the carry after the first occurrence.
    - For length == 1: center column (a==b).
    - For length == 0: no columns; carry-out equals carry-in.
    """
    if length == 0:
        return (1, 0) if carry_in == 0 else (0, 1)

    if length == 1:
        c0 = c1 = 0
        for a in range(10):
            s = a + a + carry_in
            if s % 2 == 1:  # digit must be odd
                (c0, c1)[s // 10]  # just to compute index
                if s // 10 == 0:
                    c0 += 1
                else:
                    c1 += 1
        return (c0, c1)

    # length >= 2
    total0 = total1 = 0
    for a, b in pair_generator(constrained_outer):
        s1 = a + b + carry_in          # rightmost column with incoming carry
        if s1 % 2 == 0:
            continue                   # must be odd
        inner_carry = s1 // 10
        inner0, inner1 = count_ways(length - 2, inner_carry, False)

        # mirrored leftmost column uses the same (a,b) with carry m from inner part
        s_m0 = a + b + 0
        if s_m0 % 2 == 1:
            if s_m0 // 10 == 0:
                total0 += inner0
            else:
                total1 += inner0

        s_m1 = a + b + 1
        if s_m1 % 2 == 1:
            if s_m1 // 10 == 0:
                total0 += inner1
            else:
                total1 += inner1

    return (total0, total1)

# Sum counts for all digit lengths 1..9 (numbers below 10^9)
answer = 0
for d in range(1, 10):
    answer += sum(count_ways(d, 0, True))

print(answer)
