import multiprocessing


def ways1(X):
    """
    Number of ways to form sum X using two digits d_1, d_k.
    Leading zeroes are NOT allowed, so d_1 >= 1 and d_k >= 1.
    """
    if X <= 9:
        return max(0, X - 1)
    return max(0, 19 - X)


def ways2(X):
    """
    Number of ways to form sum X using two digits d_i, d_{k+1-i}.
    Zeroes are allowed, so d_i >= 0 and d_{k+1-i} >= 0.
    """
    if X <= 9:
        return X + 1
    return 19 - X


def ways3(X):
    """
    Number of ways to form sum X using the same center digit d_i + d_i = X.
    """
    if X % 2 == 0 and 0 <= X <= 18:
        return 1
    return 0


def solve_k(k):
    """
    Explores the state space of pairs (X_1, X_2... X_m) and counts valid reversible
    numbers for exactly k digits. Evaluates carries similarly to standard addition.
    """
    if k == 1:
        return 0

    m = k // 2
    total = 0
    stack = [([], 1)]

    if k % 2 == 0:
        while stack:
            S_half, ways = stack.pop()
            # Once we constructed the mirrored sums, validate the carries
            if len(S_half) == m:
                S = S_half + S_half[::-1]
                c = 0
                valid = True
                for x in S:
                    if (x + c) % 2 == 0:
                        valid = False
                        break
                    c = (x + c) // 10
                if valid:
                    total += ways
                continue

            idx = len(S_half)
            for X in range(19):
                w = ways1(X) if idx == 0 else ways2(X)
                if w > 0:
                    stack.append((S_half + [X], ways * w))
    else:
        while stack:
            S_half, ways = stack.pop()
            # For odd length, the center digit sits alone in the middle
            if len(S_half) == m + 1:
                S = S_half + S_half[:-1][::-1]
                c = 0
                valid = True
                for x in S:
                    if (x + c) % 2 == 0:
                        valid = False
                        break
                    c = (x + c) // 10
                if valid:
                    total += ways
                continue

            idx = len(S_half)
            for X in range(19):
                if idx == 0:
                    w = ways1(X)
                elif idx == m:
                    w = ways3(X)
                else:
                    w = ways2(X)

                if w > 0:
                    stack.append((S_half + [X], ways * w))

    return total


if __name__ == '__main__':
    # 10^9 translates to numbers with up to 9 digits.
    # Distribute the workload for k = 1 through 9 across processes
    with multiprocessing.Pool(processes=9) as pool:
        results = pool.map(solve_k, range(1, 10))

    print(sum(results))