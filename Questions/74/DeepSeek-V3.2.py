import sys
from array import array

def solve() -> None:
    # factorials of digits 0..9
    fact = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]

    # maximum possible digit‑factorial sum for numbers below 1_000_000
    MAX = 2540160          # 7 * 9!

    # next_num[x] = sum of factorials of digits of x, for 0 <= x <= MAX
    next_num = array('I', [0]) * (MAX + 1)
    for i in range(10):
        next_num[i] = fact[i]
    for i in range(10, MAX + 1):
        next_num[i] = next_num[i // 10] + fact[i % 10]

    # cache for chain lengths; 0 means "not yet computed"
    cache = bytearray(MAX + 1)

    # process all starting numbers below 1_000_000
    for n in range(1, 1000000):
        if cache[n] != 0:
            continue

        path = []          # numbers in the current chain (in order)
        pos = {}           # number -> index in path
        cur = n

        while cache[cur] == 0:
            if cur in pos:                     # cycle detected
                idx = pos[cur]
                cycle_len = len(path) - idx
                # numbers inside the cycle all have the same chain length
                for j in range(idx, len(path)):
                    cache[path[j]] = cycle_len
                # numbers before the cycle
                for j in range(idx - 1, -1, -1):
                    cache[path[j]] = cache[path[j + 1]] + 1
                break

            path.append(cur)
            pos[cur] = len(path) - 1
            cur = next_num[cur]
        else:
            # we reached a number whose chain length is already known
            length = cache[cur]
            for num in reversed(path):
                length += 1
                cache[num] = length

    # count starting numbers with exactly 60 non‑repeating terms
    count = 0
    for n in range(1, 1000000):
        if cache[n] == 60:
            count += 1

    print(count)


if __name__ == "__main__":
    solve()