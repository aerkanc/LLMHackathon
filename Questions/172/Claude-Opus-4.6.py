from fractions import Fraction
import math

def poly_mul(a, b, max_deg):
    result = [Fraction(0)] * (max_deg + 1)
    la = min(len(a), max_deg + 1)
    lb = min(len(b), max_deg + 1)
    for i in range(la):
        if a[i] == 0:
            continue
        for j in range(min(lb, max_deg + 1 - i)):
            result[i + j] += a[i] * b[j]
    return result

def poly_pow(p, n, max_deg):
    result = [Fraction(1)] + [Fraction(0)] * max_deg
    base = p[:min(len(p), max_deg + 1)]
    while n > 0:
        if n & 1:
            result = poly_mul(result, base, max_deg)
        base = poly_mul(base, base, max_deg)
        n >>= 1
    return result

# EGF for digit appearing at most 3 times
p = [Fraction(1), Fraction(1), Fraction(1, 2), Fraction(1, 6)]

# Total 18-char strings (digits 0-9, each at most 3 times)
# = 18! * [x^18] p(x)^10
p10 = poly_pow(p, 10, 18)
total = p10[18] * math.factorial(18)

# Strings starting with 0: first digit fixed as 0
# Remaining 17 digits: 0 can appear at most 2 more times, others at most 3
# = 17! * [x^17] q(x) * p(x)^9
# where q(x) = 1 + x + x^2/2! (EGF for 0 with at most 2 more)
q = [Fraction(1), Fraction(1), Fraction(1, 2)]
p9 = poly_pow(p, 9, 17)
qp9 = poly_mul(q, p9, 17)
leading_zero = qp9[17] * math.factorial(17)

answer = int(total - leading_zero)
print(answer)