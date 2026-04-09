from decimal import Decimal, getcontext

getcontext().prec = 50

total = 0
for m in range(2, 16):
    # Optimal x_k = 2k/(m+1)
    # P_m = product of (2k/(m+1))^k for k=1..m
    d = Decimal(m + 1)
    log_p = Decimal(0)
    p = Decimal(1)
    for k in range(1, m + 1):
        ratio = Decimal(2 * k) / d
        p *= ratio ** k
    total += int(p)

print(total)