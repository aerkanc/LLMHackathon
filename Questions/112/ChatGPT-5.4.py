def is_bouncy(n: int) -> bool:
    s = str(n)
    inc = True
    dec = True

    for i in range(1, len(s)):
        if s[i] > s[i - 1]:
            dec = False
        elif s[i] < s[i - 1]:
            inc = False

        if not inc and not dec:
            return True

    return False


def main():
    bouncy = 0
    n = 99

    while True:
        n += 1
        if is_bouncy(n):
            bouncy += 1
        if bouncy * 100 == 99 * n:
            print(n)
            return


if __name__ == "__main__":
    main()