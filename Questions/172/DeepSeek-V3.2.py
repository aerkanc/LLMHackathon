import math

def main() -> None:
    # factorials up to 17
    fact = [1] * 18
    for i in range(1, 18):
        fact[i] = fact[i-1] * i

    fact9 = fact[9]          # 362880
    fact17 = fact[17]        # 355687428096000

    total = 0

    # d = number of digits (other than 0) with frequency 3
    for d in range(0, 7):    # 3*6 = 18, so d <= 6
        max_c = (18 - 3 * d) // 2
        for c in range(0, max_c + 1):
            b = 18 - 2 * c - 3 * d
            if b < 0:
                continue
            k = b + c + d          # number of non‑zero frequencies among all 10 digits
            if k > 10:
                continue
            a = 10 - k             # number of digits with frequency 0

            # base = 17! / (2^c * 6^d)
            base = fact17 // ((1 << c) * (6 ** d))

            # case: digit 0 has frequency 0
            if k <= 9:
                comb0 = fact9 // (fact[b] * fact[c] * fact[d] * fact[9 - k])
                total += comb0 * 18 * base

            # case: digit 0 has frequency 1
            if b >= 1:
                comb1 = fact9 // (fact[b-1] * fact[c] * fact[d] * fact[a])
                total += comb1 * 17 * base

            # case: digit 0 has frequency 2
            if c >= 1:
                comb2 = fact9 // (fact[b] * fact[c-1] * fact[d] * fact[a])
                total += comb2 * 16 * base

            # case: digit 0 has frequency 3
            if d >= 1:
                comb3 = fact9 // (fact[b] * fact[c] * fact[d-1] * fact[a])
                total += comb3 * 15 * base

    print(total)

if __name__ == "__main__":
    main()