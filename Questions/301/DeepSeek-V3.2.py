# Count positive integers n ≤ 2^30 such that n xor (2n) xor (3n) = 0.
# The condition is equivalent to n having no adjacent 1s in binary.
# The count for numbers from 0 to 2^30 - 1 inclusive is the Fibonacci number F_{32}.
# Compute F_{32} using an iterative loop.

def main():
    a, b = 0, 1  # F0, F1
    for _ in range(32):
        a, b = b, a + b
    print(a)  # a = F_{32} = 2178309

if __name__ == "__main__":
    main()