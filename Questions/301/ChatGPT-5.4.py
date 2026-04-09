def count_no_adjacent_ones_upto(limit: int) -> int:
    bits = list(map(int, bin(limit)[2:]))
    n = len(bits)

    # dp[len] = number of binary strings of length len with no consecutive 1s
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 2
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    ans = 0
    prev_bit = 0

    for i, bit in enumerate(bits):
        if bit == 1:
            remaining = n - i - 1
            ans += dp[remaining]
            if prev_bit == 1:
                return ans
            prev_bit = 1
        else:
            prev_bit = 0

    return ans + 1  # include limit itself if valid


LIMIT = 1 << 30

# X(n, 2n, 3n) = 0  <=>  n xor (2n) xor (3n) = 0
# Since 3n = n + 2n, this is equivalent to n + 2n = n xor 2n,
# which holds exactly when there is no carry in adding n and 2n.
# Because 2n is n shifted left by one bit, this means n has no adjacent 1s in binary.

result = count_no_adjacent_ones_upto(LIMIT) - 1  # exclude 0
print(result)