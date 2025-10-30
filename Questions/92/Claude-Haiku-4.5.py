def square_digit_sum(n):
    """Calculate the sum of squares of digits of n."""
    total = 0
    while n > 0:
        digit = n % 10
        total += digit * digit
        n //= 10
    return total


# Global memoization dictionary
memo = {1: False, 89: True}


def reaches_89(n):
    """Check if n reaches 89 in the square digit chain, using memoization."""
    if n in memo:
        return memo[n]

    path = []
    while n not in memo and n != 1 and n != 89:
        path.append(n)
        n = square_digit_sum(n)

    # Determine the result
    if n == 89:
        result = True
    elif n == 1:
        result = False
    else:
        result = memo[n]

    # Memoize all numbers in the path
    for num in path:
        memo[num] = result

    return result


# Count numbers below 10 million that reach 89
count = 0
for i in range(1, 10000000):
    if reaches_89(i):
        count += 1

print(count)