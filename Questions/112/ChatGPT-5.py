def is_bouncy(n: int) -> bool:
    s = str(n)
    inc = True  # non-decreasing
    dec = True  # non-increasing
    for i in range(1, len(s)):
        if s[i] < s[i - 1]:
            inc = False
        if s[i] > s[i - 1]:
            dec = False
        if not inc and not dec:
            return True
    return False  # either increasing or decreasing (or both – all equal)

def solve(target_percent: int = 99) -> int:
    bouncy = 0
    n = 0
    while True:
        n += 1
        if n >= 100 and is_bouncy(n):
            bouncy += 1
        # proportion == target_percent%
        if bouncy * 100 == target_percent * n:
            return n

print(solve(99))
