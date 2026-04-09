import sys

def solve() -> None:
    # Precompute digit pair counts for a given sum S (0..18)
    # unconstrained: a,b in 0..9
    unconstrained = [0] * 19
    # constrained: a,b in 1..9 (first and last digit)
    constrained = [0] * 19

    for s in range(19):
        if s <= 9:
            unconstrained[s] = s + 1
        else:
            unconstrained[s] = 19 - s

        if 2 <= s <= 18:
            if s <= 10:
                constrained[s] = s - 1
            else:
                constrained[s] = 19 - s
        else:
            constrained[s] = 0

    # Allowed digit sums for a column, given (carry_in, carry_out)
    allowed = {
        (0, 0): [1, 3, 5, 7, 9],
        (1, 0): [0, 2, 4, 6, 8],
        (0, 1): [11, 13, 15, 17],
        (1, 1): [10, 12, 14, 16, 18]
    }

    total = 0

    # Lengths 1 to 9, but L=1 contributes 0
    for L in range(2, 10):
        p = L // 2          # number of digit pairs
        odd = L % 2         # whether length is odd
        total_L = 0

        # Enumerate all carry sequences c2..c_{L+1} (c1 = 0)
        for mask in range(1 << L):
            # Build carry array c[1..L+1] (1-indexed)
            c = [0] * (L + 2)
            c[1] = 0
            for bit in range(L):
                c[2 + bit] = (mask >> bit) & 1

            prod = 1
            # Process digit pairs from the ends inward
            for k in range(p):
                i = k + 1
                j = L - k
                # Carries for the two columns
                cin_i, cout_i = c[i], c[i + 1]
                cin_j, cout_j = c[j], c[j + 1]

                set_i = allowed[(cin_i, cout_i)]
                set_j = allowed[(cin_j, cout_j)]

                # Use constrained counts for the outermost pair (k==0)
                cnt = constrained if k == 0 else unconstrained

                # Intersection of the two sets of allowed sums
                set_j_set = set(set_j)
                ways = 0
                for s in set_i:
                    if s in set_j_set:
                        ways += cnt[s]

                if ways == 0:
                    prod = 0
                    break
                prod *= ways

            if prod == 0:
                continue

            # Middle digit for odd lengths
            if odd:
                mid = (L + 1) // 2
                # middle digit works only when the incoming carry is 1
                if c[mid] == 1:
                    prod *= 5   # exactly 5 possibilities for the middle digit
                else:
                    prod = 0

            total_L += prod

        total += total_L

    # Output the result
    print(total)


if __name__ == "__main__":
    solve()