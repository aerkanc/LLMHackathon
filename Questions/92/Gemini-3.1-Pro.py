def solve():
    # The maximum sum of the squares of the digits for a number below 10,000,000
    # (which is 9,999,999) is 7 * 9^2 = 7 * 81 = 567.
    max_sum = 567

    # Precompute whether each number from 1 to max_sum arrives at 89
    leads_to_89 = [False] * (max_sum + 1)
    for i in range(1, max_sum + 1):
        n = i
        while n != 1 and n != 89:
            temp = 0
            while n > 0:
                d = n % 10
                temp += d * d
                n //= 10
            n = temp
        if n == 89:
            leads_to_89[i] = True

    # Use dynamic programming to count the frequency of each digit-square-sum
    # for all 7-digit combinations (from 0000000 to 9999999).
    dp = [0] * (max_sum + 1)
    dp[0] = 1  # 1 way to have a sum of 0 with 0 digits

    for _ in range(7):
        new_dp = [0] * (max_sum + 1)
        for d in range(10):
            d2 = d * d
            for v in range(max_sum + 1 - d2):
                new_dp[v + d2] += dp[v]
        dp = new_dp

    # Sum the frequencies of all sums that eventually lead to 89
    ans = 0
    for s in range(1, max_sum + 1):
        if leads_to_89[s]:
            ans += dp[s]

    print(ans)


if __name__ == '__main__':
    solve()