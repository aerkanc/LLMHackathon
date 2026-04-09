import itertools

def solve():
    def count_pairs(s, outer=False):
        """Count (a,b) digit pairs with a+b=s. If outer, both a>=1 and b>=1."""
        if outer:
            lo = max(1, s - 9)
            hi = min(9, s - 1)
        else:
            lo = max(0, s - 9)
            hi = min(9, s)
        return max(0, hi - lo + 1)

    total = 0
    for k in range(1, 10):  # 1 to 9 digit numbers
        m = k // 2           # number of digit pairs
        has_middle = k % 2 == 1

        # Build ranges for pair sums: outer pair sum in [2,18], inner in [0,18]
        ranges = []
        for i in range(m):
            ranges.append(range(2, 19) if i == 0 else range(0, 19))

        count_k = 0
        for sums in itertools.product(*ranges):
            # Compute number of digit-pair assignments for these sums
            ways = 1
            valid = True
            for i, s in enumerate(sums):
                c = count_pairs(s, outer=(i == 0))
                if c == 0:
                    valid = False
                    break
                ways *= c
            if not valid:
                continue

            # Enumerate middle digit if odd number of digits
            mid_range = range(10) if has_middle else [None]
            for mid in mid_range:
                # Build full position-sum sequence (right to left in the addition)
                # Pairs appear: s0, s1, ..., s_{m-1}, [2*mid], s_{m-1}, ..., s1, s0
                if has_middle:
                    full = list(sums) + [2 * mid] + list(reversed(sums))
                else:
                    full = list(sums) + list(reversed(sums))

                # Simulate carry chain, check all result digits are odd
                carry = 0
                ok = True
                for s in full:
                    val = s + carry
                    if val % 10 % 2 == 0:
                        ok = False
                        break
                    carry = val // 10

                if ok:
                    count_k += ways

        total += count_k

    print(total)

solve()