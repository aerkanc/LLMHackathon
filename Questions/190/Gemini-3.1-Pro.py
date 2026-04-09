from decimal import Decimal, getcontext

# Set sufficient precision for exact fractional arithmetic
getcontext().prec = 100

def compute_P(m):
    P = Decimal(1)
    for k in range(1, m + 1):
        # Optimal x_k derived from AM-GM inequality
        x_k = Decimal(2 * k) / Decimal(m + 1)
        P *= x_k ** k
    return int(P)  # int() inherently acts as a floor function for positive numbers

def solve():
    total_sum = sum(compute_P(m) for m in range(2, 16))
    print(total_sum)

if __name__ == '__main__':
    solve()