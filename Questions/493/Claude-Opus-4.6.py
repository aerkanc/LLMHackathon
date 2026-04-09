from math import comb

# By linearity of expectation:
# E[distinct colors] = 7 * (1 - C(60,20)/C(70,20))
result = 7 * (1 - comb(60, 20) / comb(70, 20))
print(f"{result:.9f}")