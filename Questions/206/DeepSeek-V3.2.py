import math

def matches(n: int) -> bool:
    """Return True if n^2 matches the pattern 1_2_3_4_5_6_7_8_9_0."""
    s = n * n
    # Check digits from the right at positions that are fixed in the pattern.
    # The required digits are: 8 (10^4), 7 (10^6), 6 (10^8), 5 (10^10),
    # 4 (10^12), 3 (10^14), 2 (10^16), 1 (10^18).
    if (s // 10000) % 10 != 8:
        return False
    if (s // 1_000_000) % 10 != 7:
        return False
    if (s // 100_000_000) % 10 != 6:
        return False
    if (s // 10_000_000_000) % 10 != 5:
        return False
    if (s // 1_000_000_000_000) % 10 != 4:
        return False
    if (s // 100_000_000_000_000) % 10 != 3:
        return False
    if (s // 10_000_000_000_000_000) % 10 != 2:
        return False
    if (s // 1_000_000_000_000_000_000) % 10 != 1:
        return False
    return True


def main() -> None:
    # Smallest and largest numbers that match the pattern (underscores = 0 and 9)
    min_sq = 1_020_304_050_607_080_900
    max_sq = 1_929_394_959_697_989_990

    # Integer square roots (floor)
    L = math.isqrt(min_sq)
    if L * L < min_sq:
        L += 1
    U = math.isqrt(max_sq)

    # The square ends with 00, so the number must end with 30 or 70.
    for residue in (30, 70):
        # Smallest t such that 100*t + residue >= L
        t_min = (L - residue + 99) // 100 if L > residue else 0
        # Largest t such that 100*t + residue <= U
        t_max = (U - residue) // 100

        for t in range(t_min, t_max + 1):
            n = 100 * t + residue
            if matches(n):
                print(n)
                return


if __name__ == "__main__":
    main()