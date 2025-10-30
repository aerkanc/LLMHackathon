#!/usr/bin/env python3

def is_bouncy(n):
    """
    Checks if a number is bouncy.
    A number is bouncy if it is neither increasing nor decreasing.
    e.g., 155349 is bouncy (1<5, 5>3)
    e.g., 134468 is not bouncy (increasing)
    e.g., 66420 is not bouncy (decreasing)
    """
    s = str(n)

    # Numbers with 1 or 2 digits cannot be bouncy.
    if len(s) < 3:
        return False

    has_increase = False
    has_decrease = False

    for i in range(len(s) - 1):
        if s[i] < s[i + 1]:
            has_increase = True
        elif s[i] > s[i + 1]:
            has_decrease = True

        # Optimization: if we've found both an increase and a decrease,
        # we know it's bouncy and can stop early.
        if has_increase and has_decrease:
            return True

    # If the loop finishes, the number was not bouncy.
    # It was either purely increasing, purely decreasing, or all same digits.
    return False


def find_target_proportion():
    """
    Finds the least number 'n' for which the proportion of bouncy
    numbers up to 'n' is exactly 99%.
    """

    # We start from the fact given in the problem:
    # "Clearly there cannot be any bouncy numbers below one-hundred."
    # So, we can start our count at n=99, where the bouncy_count is 0.
    n = 99
    bouncy_count = 0

    target_numerator = 99
    target_denominator = 100

    # We are looking for the point where:
    # bouncy_count / n = 99 / 100
    # or
    # bouncy_count * 100 == n * 99

    while True:
        n += 1

        if is_bouncy(n):
            bouncy_count += 1

        # Check if the proportion is exactly 99%
        # This integer-only comparison avoids any floating-point issues.
        if bouncy_count * target_denominator == n * target_numerator:
            # We found the least number. Print only the final result.
            print(n)
            break


if __name__ == "__main__":
    find_target_proportion()
