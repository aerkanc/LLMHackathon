import math


def calculate_Pm(m):
    """Calculate the maximum value of P_m for a given m"""
    exponent = m * (m + 1) // 2

    # Calculate numerator: 2^(m(m+1)/2) × ∏_{i=1}^m i^i
    numerator = 2 ** exponent
    for i in range(1, m + 1):
        numerator *= i ** i

    # Calculate denominator: (m+1)^(m(m+1)/2)
    denominator = (m + 1) ** exponent

    # P_m = numerator / denominator
    return numerator / denominator


def main():
    total_sum = 0
    for m in range(2, 16):
        P_m = calculate_Pm(m)
        total_sum += math.floor(P_m)

    print(int(total_sum))


if __name__ == "__main__":
    main()