def is_bouncy(n: int) -> bool:
    """Return True if n is a bouncy number (neither increasing nor decreasing)."""
    if n < 100:
        return False
    prev = n % 10
    n //= 10
    inc = True   # assume increasing (digits non‑decreasing left to right)
    dec = True   # assume decreasing (digits non‑increasing left to right)
    while n:
        cur = n % 10
        if cur > prev:
            inc = False
        elif cur < prev:
            dec = False
        if not inc and not dec:
            return True
        prev = cur
        n //= 10
    return False

def main() -> None:
    n = 1
    bouncy_cnt = 0
    while True:
        if n >= 100 and is_bouncy(n):
            bouncy_cnt += 1
        if n >= 100 and 100 * bouncy_cnt == 99 * n:
            print(n)
            return
        n += 1

if __name__ == "__main__":
    main()