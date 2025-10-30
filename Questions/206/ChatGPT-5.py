import math

def is_match(sq: int) -> bool:
    # sq ends with ...9_0; we've already ensured the trailing 0 by choosing candidates.
    sq //= 10  # drop the last fixed '0'
    # Now the digits (from right to left, every other digit) must be 9,8,7,6,5,4,3,2,1
    for expected in range(9, 0, -1):
        if sq % 10 != expected:
            return False
        sq //= 100  # skip the '_' digit
    return True

def main():
    # Bounds from the pattern 1_2_3_4_5_6_7_8_9_0
    lo = math.isqrt(1020304050607080900)
    hi = math.isqrt(1929394959697989990)

    # Only candidates ending with 30 or 70 can give a square ending with ...900
    # Align start to the first number ≥ lo that ends with 30 or 70
    n = lo - (lo % 100) + 30
    if n < lo:
        n += 40  # move to 70
    step_pair = (60, 40)  # alternate: ...30 -> +40 -> ...70 -> +60 -> ...30 ...

    i = 0
    while n <= hi:
        sq = n * n
        if is_match(sq):
            print(n)
            return
        n += step_pair[i & 1]
        i += 1

if __name__ == "__main__":
    main()
