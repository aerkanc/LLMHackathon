#!/usr/bin/env python3
"""
Project Euler Problem 502: Counting Castles

Solution using Dynamic Programming for computing F(w, h).

A castle is a configuration of stacked rectangular blocks with these rules:
1. Bottom row has one block of length w
2. Blocks in upper rows must be supported (no hanging)
3. Blocks in same row need at least 1-unit gaps
4. Total blocks must be even
5. Maximum height is exactly h (h rows total)

For w <= 20, we use bitmask DP where each row configuration is represented as
a bitmask indicating occupied positions.
"""


def count_blocks_in_config(mask, w):
    """Count the number of blocks (maximal runs of 1-bits) in a configuration."""
    count = 0
    i = 0
    while i < w:
        if mask & (1 << i):
            count += 1
            while i < w and (mask & (1 << i)):
                i += 1
        else:
            i += 1
    return count


def solve_F(w, h, use_modulo=False):
    """
    Compute F(w, h) = number of valid castles with width w and height h.

    Args:
        w: Grid width (must be <= 20 for bitmask approach)
        h: Grid height
        use_modulo: If True, apply mod 1000000007 to final result

    Returns:
        F(w, h) or F(w, h) % 1000000007
    """
    MOD = 1000000007

    if w > 20:
        raise ValueError("solve_F only supports w <= 20 (bitmask approach)")

    def count_blocks(mask):
        return count_blocks_in_config(mask, w)

    # Generate all valid row configurations (all non-empty subsets)
    all_configs = list(range(1, 2 ** w))

    # Precompute block counts for each configuration
    blocks_in = {cfg: count_blocks(cfg) for cfg in all_configs}

    # Initialize with bottom row: completely filled (single block of width w)
    bottom = (1 << w) - 1  # All bits set
    bottom_blocks = blocks_in[bottom]  # Always 1
    bottom_parity = bottom_blocks % 2  # Always odd (1 % 2 = 1)

    # DP: state is (row_configuration, parity_of_total_blocks)
    # Map to count of ways to reach that state
    dp = {(bottom, bottom_parity): 1}

    # Build castle layer by layer
    for height in range(1, h):
        new_dp = {}

        for (current_config, current_parity), ways in dp.items():
            # Try all possible next-row configurations
            for next_config in all_configs:
                # Check support constraint: next block must fit within current support
                if (next_config & current_config) != next_config:
                    continue  # This configuration would hang in open space

                # Compute new parity with added blocks
                blocks_added = blocks_in[next_config]
                new_parity = (current_parity + blocks_added) % 2

                # Add to new DP state
                key = (next_config, new_parity)
                new_dp[key] = new_dp.get(key, 0) + ways

        dp = new_dp

    # Count valid castles at height h with even total blocks (parity = 0)
    result = sum(ways for (config, parity), ways in dp.items() if parity == 0)

    if use_modulo:
        return result % MOD
    else:
        return result


# Test cases from problem
print("Test cases:")
print(f"F(4, 2) = {solve_F(4, 2)} (expected: 10)")
print(f"F(13, 10) = {solve_F(13, 10)} (expected: 3729050610636)")
print(f"F(10, 13) = {solve_F(10, 13)} (expected: 37959702514)")
print()

# The main problem asks for: (F(10^12, 100) + F(100000, 100000) + F(100, 10^12)) mod 1000000007
# However, all three have w > 20, which our bitmask approach cannot handle.
#
# For large w, we would need:
# 1. Mathematical analysis of block configuration patterns
# 2. Generating functions or closed-form formulas
# 3. Advanced combinatorial techniques
#
# Since w=10^12, w=100000, and w=100 all exceed our w<=20 limit,
# we cannot compute the final answer with the current approach.

MOD = 1000000007

try:
    # These would require different algorithms:
    # result1 = solve_F(10**12, 100, use_modulo=True)  # w too large
    # result2 = solve_F(100000, 100000, use_modulo=True)  # w too large
    # result3 = solve_F(100, 10**12, use_modulo=True)  # w too large

    print("For the final answer: F(10^12, 100) + F(100000, 100000) + F(100, 10^12)")
    print("requires mathematical algorithms for large w values beyond bitmask DP.")
    print()
    print("The problem requires advanced techniques such as:")
    print("- Shape-based configuration enumeration")
    print("- Generating functions for configuration counting")
    print("- Mathematical optimization for specific problem structure")

except ValueError as e:
    print(f"Error: {e}")