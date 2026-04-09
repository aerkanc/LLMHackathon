FACT = (1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880)

LIMIT = 1_000_000
MAX_NEXT = 7 * FACT[9]  # Maximum possible value for numbers below one million

# Sum of digit factorials for 0..9999 treating numbers normally
sum_var = [0] * 10000
for i in range(1, 10000):
    sum_var[i] = sum_var[i // 10] + FACT[i % 10]

# Sum of digit factorials for 0..9999 treating each value as exactly 4 digits
sum_fixed4 = [0] * 10000
base = 4 * FACT[0]
for i in range(10000):
    if i == 0:
        sum_fixed4[i] = base
    else:
        x = i
        s = 0
        digits = 0
        while x:
            s += FACT[x % 10]
            x //= 10
            digits += 1
        sum_fixed4[i] = s + (4 - digits) * FACT[0]

# Next value in the chain
nxt = [0] * (MAX_NEXT + 1)
for n in range(MAX_NEXT + 1):
    if n < 10000:
        nxt[n] = sum_var[n]
    else:
        nxt[n] = sum_var[n // 10000] + sum_fixed4[n % 10000]

# chain_len[n] = number of non-repeating terms starting from n
chain_len = [0] * (MAX_NEXT + 1)

for start in range(1, MAX_NEXT + 1):
    if chain_len[start]:
        continue

    path = []
    pos = {}
    x = start

    while True:
        known = chain_len[x]
        if known:
            length = known
            for v in reversed(path):
                length += 1
                chain_len[v] = length
            break

        if x in pos:
            loop_start = pos[x]
            loop_len = len(path) - loop_start

            for i in range(loop_start, len(path)):
                chain_len[path[i]] = loop_len

            length = loop_len
            for i in range(loop_start - 1, -1, -1):
                length += 1
                chain_len[path[i]] = length
            break

        pos[x] = len(path)
        path.append(x)
        x = nxt[x]

count = 0
for n in range(1, LIMIT):
    if chain_len[n] == 60:
        count += 1

print(count)