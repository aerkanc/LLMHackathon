def main():
    total = 0

    for m in range(2, 16):
        s = m * (m + 1) // 2

        numerator = 1 << s  # 2^s
        for i in range(1, m + 1):
            numerator *= pow(i, i)

        denominator = pow(m + 1, s)
        total += numerator // denominator

    print(total)

main()