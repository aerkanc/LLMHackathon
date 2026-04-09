import math


def solve():
    # Maximum possible sum of digit factorials for a number < 3,000,000
    # is for 2,999,999 -> 2! + 6 * 9! = 2 + 2177280 = 2177282.
    # Therefore, 3,000,000 is a safe upper bound.
    limit = 3000000
    facts = [math.factorial(i) for i in range(10)]

    # Precompute the sum of the factorial of digits for each number
    next_val = [0] * limit
    for i in range(10):
        next_val[i] = facts[i]
    for i in range(10, limit):
        next_val[i] = next_val[i // 10] + facts[i % 10]

    # Array to memoize the chain length of each number
    memo = [0] * limit
    count = 0

    # Process all starting numbers below one million
    for i in range(1000000):
        curr = i
        chain = []

        while memo[curr] == 0:
            try:
                # Check if we hit a loop within the current progressing chain
                idx = chain.index(curr)

                # Found a new loop
                loop_len = len(chain) - idx

                # Length for elements before the loop
                for j in range(idx):
                    memo[chain[j]] = len(chain) - j

                # Length for elements within the loop
                for j in range(idx, len(chain)):
                    memo[chain[j]] = loop_len

                break

            except ValueError:
                # curr is not in the chain, continue adding and advancing
                chain.append(curr)
                curr = next_val[curr]
        else:
            # Reached a number whose chain length was resolved in a previous sequence
            l = memo[curr]
            for idx, val in enumerate(chain):
                memo[val] = len(chain) - idx + l

        # Only count chains originating below 1,000,000 that contain exactly 60 terms
        if memo[i] == 60:
            count += 1

    print(count)


if __name__ == '__main__':
    solve()