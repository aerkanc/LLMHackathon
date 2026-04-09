from collections import Counter

def allowed_sums(carry_in, carry_out):
    res = set()
    for s in range(19):  # max digit-pair sum is 9 + 9 = 18
        if ((s + carry_in) % 2 == 1) and ((1 if s + carry_in >= 10 else 0) == carry_out):
            res.add(s)
    return res

def build_sum_counts():
    outer = Counter()
    inner = Counter()
    middle = Counter()

    # Outermost pair: both digits must be nonzero
    for a in range(1, 10):
        for b in range(1, 10):
            outer[a + b] += 1

    # Inner pairs: digits may be zero
    for a in range(10):
        for b in range(10):
            inner[a + b] += 1

    # Middle digit for odd length: contributes 2*d
    for d in range(10):
        middle[2 * d] += 1

    return outer, inner, middle

ALLOWED = {(cin, cout): allowed_sums(cin, cout) for cin in (0, 1) for cout in (0, 1)}
OUTER_COUNTS, INNER_COUNTS, MIDDLE_COUNTS = build_sum_counts()

def count_reversible_with_length(n):
    half = n // 2
    total = 0

    # Carry sequence c[0..n], with c[0] = 0 and c[1..n] enumerated
    for mask in range(1 << n):
        carries = [0] + [(mask >> i) & 1 for i in range(n)]

        ways = 1

        # Process mirrored digit pairs
        for i in range(1, half + 1):
            left_allowed = ALLOWED[(carries[i - 1], carries[i])]
            right_allowed = ALLOWED[(carries[n - i], carries[n - i + 1])]
            valid_sums = left_allowed & right_allowed

            counts = OUTER_COUNTS if i == 1 else INNER_COUNTS
            pair_ways = sum(counts[s] for s in valid_sums)

            if pair_ways == 0:
                ways = 0
                break

            ways *= pair_ways

        if ways == 0:
            continue

        # Middle digit for odd length
        if n % 2 == 1:
            mid = half + 1
            valid_sums = ALLOWED[(carries[mid - 1], carries[mid])]
            middle_ways = sum(cnt for s, cnt in MIDDLE_COUNTS.items() if s in valid_sums)

            if middle_ways == 0:
                continue

            ways *= middle_ways

        total += ways

    return total

def solve(limit):
    digits = len(str(limit - 1))
    ans = 0
    for n in range(1, digits + 1):
        ans += count_reversible_with_length(n)
    return ans

print(solve(10**9))