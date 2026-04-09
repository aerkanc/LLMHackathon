def is_bouncy(n):
    s = str(n)
    inc = True
    dec = True
    for i in range(1, len(s)):
        if s[i] > s[i-1]:
            dec = False
        if s[i] < s[i-1]:
            inc = False
        if not inc and not dec:
            return True
    return False

bouncy = 0
n = 1
while True:
    if is_bouncy(n):
        bouncy += 1
    if bouncy * 100 == 99 * n:
        print(n)
        break
    n += 1