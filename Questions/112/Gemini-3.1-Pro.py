def solve():
    bouncy_count = 0
    # There are no bouncy numbers below 100
    n = 99

    while True:
        n += 1
        temp = n
        last = temp % 10
        temp //= 10
        inc = False
        dec = False

        # Check digits from right to left using fast integer math
        while temp > 0:
            d = temp % 10
            if d < last:
                inc = True
                if dec:
                    bouncy_count += 1
                    break
            elif d > last:
                dec = True
                if inc:
                    bouncy_count += 1
                    break
            last = d
            temp //= 10

        # Cross-multiply to avoid floating point precision issues:
        # bouncy_count / n == 99 / 100  =>  bouncy_count * 100 == 99 * n
        if bouncy_count * 100 == 99 * n:
            print(n)
            break


if __name__ == '__main__':
    solve()