def solve():
    fact = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]

    def digit_fact_sum(n):
        s = 0
        while n > 0:
            s += fact[n % 10]
            n //= 10
        return s

    chain_len = {}
    count = 0

    for n in range(1, 1_000_000):
        seen = []
        seen_set = set()
        cur = n
        while cur not in seen_set and cur not in chain_len:
            seen_set.add(cur)
            seen.append(cur)
            cur = digit_fact_sum(cur)

        if cur in chain_len:
            base = chain_len[cur]
        else:
            loop_start = seen.index(cur)
            loop_size = len(seen) - loop_start
            for i in range(loop_start, len(seen)):
                chain_len[seen[i]] = loop_size
            base = loop_size
            for i in range(loop_start - 1, -1, -1):
                base += 1
                chain_len[seen[i]] = base
            if chain_len[n] == 60:
                count += 1
            continue

        for i in range(len(seen) - 1, -1, -1):
            base += 1
            chain_len[seen[i]] = base

        if chain_len[n] == 60:
            count += 1

    print(count)

solve()