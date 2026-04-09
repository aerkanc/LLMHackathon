import sys

def compute_floor_pm(m: int) -> int:
    """
    Compute floor(P_m) where P_m = ∏_{i=1}^{m} (2i/(m+1))^i.
    """
    S = m * (m + 1) // 2          # sum of exponents
    prod = 1
    for i in range(1, m + 1):
        prod *= i ** i
    numerator = (2 ** S) * prod
    denominator = (m + 1) ** S
    return numerator // denominator

def main() -> None:
    total = 0
    for m in range(2, 16):        # m = 2 .. 15
        total += compute_floor_pm(m)
    print(total)

if __name__ == "__main__":
    main()