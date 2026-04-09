def solve():
    limit = 10_000_000
    # Max sum of squared digits for 9_999_999 = 7*81 = 567
    # Precompute which numbers 1..567 end at 89
    cache = [0] * 568
    for i in range(1, 568):
        n = i
        while n != 1 and n != 89:
            s = 0
            while n:
                n, d = divmod(n, 10)
                s += d * d
            n = s
        cache[i] = 1 if n == 89 else 0

    count = 0
    for n in range(1, limit):
        s = 0
        tmp = n
        while tmp:
            tmp, d = divmod(tmp, 10)
            s += d * d
        if cache[s]:
            count += 1
    print(count)

solve()