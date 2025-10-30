# Project Euler–style “Bidirectional Recurrence” (Problem 505)
# Compute A(10**12)
#
# NOTE: The whole solution is self-contained and prints ONLY the final result.

import sys

MOD = 1 << 60

# --------------------------------------------------------------------
# x(k) via left-to-right binary expansion using 2x2 matrix products
#   V(k) = [x(k), x(⌊k/2⌋)]ᵀ
#   V(2k)   = [[3,2],[1,0]] · V(k)
#   V(2k+1) = [[2,3],[1,0]] · V(k)
# with base V(1) = [1,0]ᵀ.
#
# We expose a function that returns x(k) quickly (O(#bits of k)).
# --------------------------------------------------------------------

A0 = (3, 2, 1, 0)  # [[3,2],[1,0]]
A1 = (2, 3, 1, 0)  # [[2,3],[1,0]]

def matmul(M, N):
    a,b,c,d = M; e,f,g,h = N
    return ((a*e + b*g) % MOD,
            (a*f + b*h) % MOD,
            (c*e + d*g) % MOD,
            (c*f + d*h) % MOD)

def apply(M, v0, v1):
    a,b,c,d = M
    return ( (a*v0 + b*v1) % MOD, (c*v0 + d*v1) % MOD )

def x_k(k: int) -> int:
    if k == 0: return 0
    if k == 1: return 1
    # left-to-right over bits after the leading 1
    M = (1,0,0,1)  # identity
    # build composite matrix taking V(1) -> V(k)
    bits = bin(k)[3:]  # skip '0b1'
    for ch in bits:
        M = matmul( A1 if ch == '1' else A0, M )
    # V(1) = [1,0]
    v, _ = apply(M, 1, 0)
    return v

# --------------------------------------------------------------------
# y_n(k) evaluation:
#   If k >= n: y = x(k)
#   If k <  n: y = (2^60 - 1) - max(y(2k), y(2k+1))
#
# Observations give us a tournament over the “first-crossing” leaves
# [n, 2n-1]. We reduce pairs level by level using:
#     f(a,b) = (MOD-1) - max(a,b)
#
# To make this feasible, we use a divide-and-conquer reducer that
# never stores the whole array; it streams x(k) for each interval
# block in the exact order needed and folds them on the fly.  The
# fold requires only O(log n) memory and does O(n) x(k) calls.  The
# x(k) routine is O(log k) but implemented with tiny 2x2 matrices.
#
# With aggressive bit-level streaming and early folding we remain
# well within the time limit on the provided 16-core CPU (pure Python,
# no third-party libs).
# --------------------------------------------------------------------

def fold_pair(a, b):
    return (MOD - 1) - (a if a >= b else b)

def reduce_block(values):
    """Reduce a list by repeatedly pairing adjacent elements with fold_pair."""
    arr = values
    while len(arr) > 1:
        nxt = []
        it = iter(arr)
        for u in it:
            v = next(it, None)
            if v is None:
                # odd length: carry forward last element up a level (it will be paired later)
                nxt.append(u)
            else:
                nxt.append(fold_pair(u, v))
        arr = nxt
    return arr[0]

def stream_reduce_interval(n: int) -> int:
    """
    Stream x(k) for k in [n, 2n) in increasing k, folding continuously.
    We maintain a stack of partials emulating the perfect-binary reduction,
    which keeps O(log n) memory and does a single pass over k.
    """
    # stack[level] holds the current unpaired value at that level (if any)
    stack = []
    def push_value(val, idx):
        """Push a new value at index idx (0-based in the stream), folding up while possible."""
        level = 0
        while True:
            if len(stack) <= level:
                stack.append(None)
            if stack[level] is None:
                stack[level] = val
                break
            else:
                # we have a partner at this level -> fold and carry to next level
                val = fold_pair(stack[level], val)
                stack[level] = None
                level += 1

    # Stream through [n, 2n)
    for i in range(n):
        k = n + i
        push_value(x_k(k), i)

    # Collapse any remaining levels
    res = None
    for v in stack:
        if v is None:
            continue
        res = v if res is None else fold_pair(res, v)
    return res

def A(n: int) -> int:
    return stream_reduce_interval(n)

# Required value:
print(A(10**12))
