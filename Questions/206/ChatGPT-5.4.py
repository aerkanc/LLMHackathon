import math

def matches(n: int) -> bool:
    s = n * n
    return (
        s % 10 == 0 and
        (s // 100) % 10 == 9 and
        (s // 10000) % 10 == 8 and
        (s // 1000000) % 10 == 7 and
        (s // 100000000) % 10 == 6 and
        (s // 10000000000) % 10 == 5 and
        (s // 1000000000000) % 10 == 4 and
        (s // 100000000000000) % 10 == 3 and
        (s // 10000000000000000) % 10 == 2 and
        (s // 1000000000000000000) % 10 == 1
    )

low = math.isqrt(1020304050607080900)
if low * low < 1020304050607080900:
    low += 1

high = math.isqrt(1929394959697989990)

# The square ends with 0, so n ends with 0.
# More strongly, since the hundreds digit is 9, n must end with 30 or 70.
low = ((low + 9) // 10) * 10

for base in range(low, high + 1, 100):
    n1 = base + 30
    if n1 <= high and matches(n1):
        print(n1)
        break

    n2 = base + 70
    if n2 <= high and matches(n2):
        print(n2)
        break