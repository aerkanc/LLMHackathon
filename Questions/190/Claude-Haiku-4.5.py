import math

def compute_pm(m):
    """
    Compute the maximum value of P_m = x_1 * x_2^2 * ... * x_m^m
    where x_i = 2*i/(m+1) is the optimal value maximizing the product
    subject to sum(x_i) = m
    """
    log_pm = 0.0
    for i in range(1, m + 1):
        x_i = 2.0 * i / (m + 1)
        log_pm += i * math.log(x_i)
    return math.exp(log_pm)

# Compute sum of floor(P_m) for m from 2 to 15
total = 0
for m in range(2, 16):
    pm = compute_pm(m)
    floor_pm = int(pm)
    total += floor_pm

print(total)