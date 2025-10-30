def count_18_digit_numbers():
    """
    Count 18-digit numbers where no digit occurs more than 3 times.
    Uses dynamic programming with memoization.
    """
    memo = {}

    def dp(pos, counts):
        """
        Recursively count valid numbers.

        Args:
            pos: Current position in the 18-digit number (0 to 17)
            counts: Tuple of 10 integers representing how many times each digit (0-9) appears so far

        Returns:
            Number of valid ways to complete the number from this state
        """
        # Base case: we've filled all 18 positions
        if pos == 18:
            return 1

        # Check memoization
        if counts in memo:
            return memo[counts]

        result = 0

        # Try placing each digit (0-9) at the current position
        for digit in range(10):
            # Skip leading zeros (position 0 cannot be 0)
            if pos == 0 and digit == 0:
                continue

            # Only place digit if it hasn't been used 3 times already
            if counts[digit] < 3:
                # Create new counts with this digit incremented
                new_counts = list(counts)
                new_counts[digit] += 1

                # Recurse to next position
                result += dp(pos + 1, tuple(new_counts))

        # Memoize and return
        memo[counts] = result
        return result

    # Start with position 0 and all digits having count 0
    initial_counts = tuple([0] * 10)
    return dp(0, initial_counts)


# Compute and print the answer
print(count_18_digit_numbers())