# Project Euler 301: Nim
# We need n XOR 2n XOR 3n = 0, i.e., n & 2n = 0
# This means n has no two consecutive 1-bits in binary.
# Count such n from 1 to 2^30.

# Numbers from 0 to 2^k - 1 with no two consecutive 1-bits
# equals a(k) where a(k) = a(k-1) + a(k-2), a(0)=1, a(1)=2
# (These are Fibonacci numbers: a(k) = F(k+2))

# For [0, 2^30-1]: a(30) values have no consecutive 1-bits
# 2^30 itself (100...0) also qualifies
# Subtract 1 for n=0 (we need positive integers)

# So answer = a(30) + 1 - 1 = a(30)

a, b = 1, 2  # a(0), a(1)
for _ in range(29):
    a, b = b, a + b
# Now b = a(30)
print(b)