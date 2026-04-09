def main():
    LIMIT_DIGITS = 7
    MAX_SUM = LIMIT_DIGITS * 81

    sq = [i * i for i in range(10)]

    # Count how many 7-digit strings (with leading zeros) have each digit-square-sum.
    dp = [0] * (MAX_SUM + 1)
    dp[0] = 1

    for _ in range(LIMIT_DIGITS):
        new_dp = [0] * (MAX_SUM + 1)
        for s, count in enumerate(dp):
            if count:
                for d in range(10):
                    new_dp[s + sq[d]] += count
        dp = new_dp

    # Determine whether each possible sum ends at 89 or 1.
    result_cache = [0] * (MAX_SUM + 1)  # 1 => ends at 1, 89 => ends at 89
    result_cache[1] = 1
    result_cache[89] = 89

    def next_sum(n: int) -> int:
        total = 0
        while n:
            n, digit = divmod(n, 10)
            total += sq[digit]
        return total

    for n in range(1, MAX_SUM + 1):
        if result_cache[n]:
            continue
        path = []
        x = n
        while not result_cache[x]:
            path.append(x)
            x = next_sum(x)
        end = result_cache[x]
        for v in path:
            result_cache[v] = end

    # Sum counts whose chains end at 89.
    # dp[0] corresponds to 0000000, which is not below ten million as a starting positive integer,
    # and it does not end at 89 anyway.
    answer = sum(dp[s] for s in range(1, MAX_SUM + 1) if result_cache[s] == 89)

    print(answer)

if __name__ == "__main__":
    main()