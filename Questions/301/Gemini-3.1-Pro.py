def solve():
    # The number of valid positive integers <= 2^k corresponds
    # to the (k+2)-th Fibonacci number where F(1)=1, F(2)=1, F(3)=2, etc.
    k = 30
    a, b = 1, 2

    for _ in range(k):
        a, b = b, a + b

    print(a)


if __name__ == '__main__':
    solve()