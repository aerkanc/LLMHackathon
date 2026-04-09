import numpy as np
import subprocess
import struct
import os
import tempfile

def main():
    N = 10**11
    MOD = 10**9
    U = int(N ** (2.0/3.0)) + 100

    # Sieve primes
    sieve = np.ones(U + 1, dtype=np.bool_)
    sieve[0] = sieve[1] = False
    for i in range(2, int(U**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = False
    primes = np.where(sieve)[0].tolist()
    del sieve

    # Mobius function via sieve
    mu = np.ones(U + 1, dtype=np.int8)
    mu[0] = 0
    for p in primes:
        mu[p::p] *= -1
        p2 = p * p
        if p2 <= U:
            mu[p2::p2] = 0
    del primes

    # F_small[n] = sum_{k=1}^n mu(k)*k mod MOD
    idx = np.arange(U + 1, dtype=np.int64)
    mk = mu.astype(np.int64) * idx
    del mu, idx
    F_small_mod = np.cumsum(mk) % MOD
    del mk

    # Write binary data for C program
    datafile = '/tmp/fdata.bin'
    with open(datafile, 'wb') as f:
        f.write(struct.pack('q', U))
        F_small_mod.astype(np.int64).tofile(f)
    del F_small_mod

    # Write C source
    c_source = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MOD 1000000000LL
#define HASH_SIZE 16384

static long long *F_small;
static long long U_val;

static long long hash_keys[HASH_SIZE];
static long long hash_vals[HASH_SIZE];
static int hash_used[HASH_SIZE];

void hash_init() { memset(hash_used, 0, sizeof(hash_used)); }

void hash_set(long long key, long long val) {
    int h = (int)((unsigned long long)(key * 2654435761ULL) & (HASH_SIZE - 1));
    while (hash_used[h]) {
        if (hash_keys[h] == key) { hash_vals[h] = val; return; }
        h = (h + 1) & (HASH_SIZE - 1);
    }
    hash_keys[h] = key; hash_vals[h] = val; hash_used[h] = 1;
}

long long hash_get(long long key) {
    int h = (int)((unsigned long long)(key * 2654435761ULL) & (HASH_SIZE - 1));
    while (hash_used[h]) {
        if (hash_keys[h] == key) return hash_vals[h];
        h = (h + 1) & (HASH_SIZE - 1);
    }
    return 0;
}

static inline long long F_mod(long long n) {
    if (n <= U_val) return F_small[n];
    return hash_get(n);
}

static inline long long P_mod(long long n) {
    long long nm = n % MOD, np1m = (n + 1) % MOD;
    if (n % 2 == 0) return (nm / 2 % MOD) * np1m % MOD;
    else return nm * (np1m / 2 % MOD) % MOD;
}

long long compute_T(long long n) {
    long long r = 0, d = 1;
    while (d <= n) {
        long long q = n / d, hi = n / q;
        long long cnt = hi - d + 1;
        long long sm;
        if ((d + hi) % 2 == 0)
            sm = ((d + hi) / 2 % MOD) * (cnt % MOD) % MOD;
        else
            sm = ((d + hi) % MOD) * (cnt / 2 % MOD) % MOD;
        r = (r + (q % MOD) * sm) % MOD;
        d = hi + 1;
    }
    return r;
}

int main(int argc, char **argv) {
    if (argc < 3) return 1;
    long long N = atoll(argv[2]);

    FILE *f = fopen(argv[1], "rb");
    if (!f) return 1;
    long long U_read;
    fread(&U_read, sizeof(long long), 1, f);
    U_val = U_read;
    F_small = (long long *)malloc((U_val + 1) * sizeof(long long));
    fread(F_small, sizeof(long long), U_val + 1, f);
    fclose(f);

    hash_init();

    long long large_vals[5000];
    int n_large = 0;
    long long k = 1;
    while (1) {
        long long v = N / k;
        if (v <= U_val) break;
        large_vals[n_large++] = v;
        k = N / v + 1;
    }
    for (int i = 0; i < n_large / 2; i++) {
        long long tmp = large_vals[i];
        large_vals[i] = large_vals[n_large - 1 - i];
        large_vals[n_large - 1 - i] = tmp;
    }

    for (int idx = 0; idx < n_large; idx++) {
        long long n = large_vals[idx];
        long long half = n / 2;
        long long res = ((1 - P_mod(n) + F_mod(half)) % MOD + MOD) % MOD;
        long long kk = 2;
        while (kk <= half) {
            long long q = n / kk;
            long long hi_k = n / q;
            if (hi_k > half) hi_k = half;
            long long df = ((F_mod(hi_k) - F_mod(kk - 1)) % MOD + MOD) % MOD;
            res = ((res - P_mod(q) * df % MOD) % MOD + MOD) % MOD;
            kk = hi_k + 1;
        }
        hash_set(n, res);
    }

    long long S = 0, d = 1;
    while (d <= N) {
        long long q = N / d, hi = N / q;
        long long Tq = compute_T(q);
        long long Fhi = F_mod(hi);
        long long Flo = (d > 1) ? F_mod(d - 1) : 0;
        long long dF = ((Fhi - Flo) % MOD + MOD) % MOD;
        if (dF != 0) S = (S + Tq * Tq % MOD * dF) % MOD;
        d = hi + 1;
    }

    printf("%lld\n", S);
    free(F_small);
    return 0;
}
'''
    c_file = '/tmp/pe439.c'
    exe_file = '/tmp/pe439'
    with open(c_file, 'w') as f:
        f.write(c_source)

    os.system(f'gcc -O2 -o {exe_file} {c_file} -lm')

    result = subprocess.run([exe_file, datafile, str(N)],
                          capture_output=True, text=True, timeout=120)
    print(result.stdout.strip())

if __name__ == '__main__':
    main()