# Maximising a Weighted Product (Euler-style) — compute sum_{m=2}^{15} floor(P_m)
# Optimal values from Lagrange multipliers: x_i = 2i/(m+1)
# Hence P_m = (∏_{i=1}^m i^i) * 2^{S} / (m+1)^{S}, where S = m(m+1)//2

total = 0
prod_i_pow_i = 1

for m in range(1, 16):
    prod_i_pow_i *= pow(m, m)  # maintain ∏ i^i cumulatively
    if m >= 2:
        S = m * (m + 1) // 2
        numerator = prod_i_pow_i << S          # multiply by 2^S using bit shift
        denominator = pow(m + 1, S)
        total += numerator // denominator       # floor(P_m)

print(total)
