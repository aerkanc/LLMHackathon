import subprocess, os, sys, tempfile

C_CODE = r"""
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

typedef uint64_t u64;
#define MASK ((1ULL << 60) - 1)

u64 N_val;
int total_depth;

#define CACHE_BITS 24
#define CACHE_SIZE (1 << CACHE_BITS)
static uint8_t order_cache[CACHE_SIZE];

static inline u64 estimate_leftmost(u64 a, u64 b, int depth) {
    int target = total_depth;
    if (target > depth + 20) target = depth + 20;
    while (depth < target) {
        u64 na = (3*a + 2*b) & MASK;
        b = a; a = na;
        depth++;
    }
    return (depth & 1) ? (MASK - a) : a;
}

u64 ab(u64 k, u64 xk, u64 xk2, int d,
       u64 alpha, u64 beta, int maximizing, int depth_left) {

    if (k >= N_val)
        return (d & 1) ? (MASK - xk) : xk;

    if (depth_left <= 0)
        return estimate_leftmost(xk, xk2, d);

    u64 xl = (3*xk + 2*xk2) & MASK;
    u64 xr = (2*xk + 3*xk2) & MASK;

    int try_right;
    int use_cache = (k < CACHE_SIZE);

    if (use_cache && order_cache[k]) {
        try_right = (order_cache[k] == 2);
    } else {
        u64 est_l = estimate_leftmost(xl, xk, d + 1);
        u64 est_r = estimate_leftmost(xr, xk, d + 1);
        try_right = maximizing ? (est_r > est_l) : (est_r < est_l);
    }

    u64 first_x, second_x, first_k, second_k;
    if (try_right) {
        first_k = 2*k+1; first_x = xr;
        second_k = 2*k;   second_x = xl;
    } else {
        first_k = 2*k;    first_x = xl;
        second_k = 2*k+1; second_x = xr;
    }

    u64 value;
    if (maximizing) {
        value = ab(first_k, first_x, xk, d+1, alpha, beta, 0, depth_left-1);
        if (value > alpha) alpha = value;
        if (alpha < beta) {
            u64 v2 = ab(second_k, second_x, xk, d+1, alpha, beta, 0, depth_left-1);
            if (v2 > value) { value = v2; try_right = !try_right; }
        }
    } else {
        value = ab(first_k, first_x, xk, d+1, alpha, beta, 1, depth_left-1);
        if (value < beta) beta = value;
        if (beta > alpha) {
            u64 v2 = ab(second_k, second_x, xk, d+1, alpha, beta, 1, depth_left-1);
            if (v2 < value) { value = v2; try_right = !try_right; }
        }
    }

    if (use_cache) order_cache[k] = try_right ? 2 : 1;
    return value;
}

int main(int argc, char **argv) {
    N_val = 1000000000000ULL;
    if (argc > 1) N_val = strtoull(argv[1], NULL, 10);

    if (N_val <= 2) total_depth = 2;
    else total_depth = 64 - __builtin_clzll(N_val - 1);

    memset(order_cache, 0, sizeof(order_cache));

    u64 result = 0;
    for (int d = 1; d <= total_depth + 1; d++) {
        result = ab(1, 1, 0, 0, 0, MASK, 0, d);
    }

    printf("%lu\n", result);
    return 0;
}
"""

tmpdir = tempfile.mkdtemp()
src = os.path.join(tmpdir, "sol.c")
exe = os.path.join(tmpdir, "sol")

with open(src, "w") as f:
    f.write(C_CODE)

subprocess.run(["gcc", "-O3", "-o", exe, src], check=True)
result = subprocess.run([exe, "1000000000000"], capture_output=True, text=True, timeout=55)
print(result.stdout.strip())