def is_bouncy(n):
    """Check if n is a bouncy number"""
    s = str(n)

    # Single digit numbers are not bouncy
    if len(s) == 1:
        return False

    # Check if the number is non-decreasing (increasing)
    is_increasing = all(s[i] <= s[i + 1] for i in range(len(s) - 1))

    # Check if the number is non-increasing (decreasing)
    is_decreasing = all(s[i] >= s[i + 1] for i in range(len(s) - 1))

    # A number is bouncy if it's neither increasing nor decreasing
    return not is_increasing and not is_decreasing


# Search for the first number where exactly 99% are bouncy
bouncy_count = 0

for n in range(1, 10000000):  # Search up to 10 million
    if is_bouncy(n):
        bouncy_count += 1

    # Check if proportion is exactly 99%
    # This is equivalent to: bouncy_count / n == 0.99
    if bouncy_count * 100 == n * 99:
        print(n)
        break