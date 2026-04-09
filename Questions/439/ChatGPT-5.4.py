MOD = 10**9
N = 10**11
B = 2_000_000

mu = [0] * (B + 1)
sigma = [0] * (B + 1)
sp_pow = [0] * (B + 1)
sp_sigma = [0] * (B + 1)
is_comp = bytearray(B + 1)
primes = []

mu[1] = 1
sigma[1] = 1
sp_pow[1] = 1
sp_sigma[1] = 1

for i in range(2, B + 1):
    if not is_comp[i]:
        primes.append(i)
        mu[i] = -1
        sp_pow[i] = i
        sp_sigma[i] = 1 + i
        sigma[i] = 1 + i
    for p in primes:
        v = i * p
        if v > B:
            break
        is_comp[v] = 1
        if i % p == 0:
            mu[v] = 0
            pp = sp_pow[i] * p
            sp_pow[v] = pp
            sp_sigma[v] = sp_sigma[i] + pp
            sigma[v] = sigma[i // sp_pow[i]] * sp_sigma[v]
            break
        else:
            mu[v] = -mu[i]
            sp_pow[v] = p
            sp_sigma[v] = 1 + p
            sigma[v] = sigma[i] * (1 + p)

M = [0] * (B + 1)   # prefix sum of mu
A = [0] * (B + 1)   # prefix sum of mu(n) * n
F = [0] * (B + 1)   # prefix sum of sigma

sm = sa = sf = 0
for i in range(1, B + 1):
    sm += mu[i]
    sa += mu[i] * i
    sf += sigma[i]
    M[i] = sm
    A[i] = sa
    F[i] = sf

vals = []
l = 1
while l <= N:
    q = N // l
    r = N // q
    if q > B:
        vals.append(q)
    l = r + 1
vals.sort()

idx = {v: i for i, v in enumerate(vals)}
MV = [0] * len(vals)
AV = [0] * len(vals)
FV = [0] * len(vals)

def tri(x):
    return x * (x + 1) // 2

def getM(x):
    return M[x] if x <= B else MV[idx[x]]

def getA(x):
    return A[x] if x <= B else AV[idx[x]]

def getF(x):
    return F[x] if x <= B else FV[idx[x]]

for ii, x in enumerate(vals):
    res = 1
    l = 2
    while l <= x:
        q = x // l
        r = x // q
        res -= (r - l + 1) * getM(q)
        l = r + 1
    MV[ii] = res

    res = 1
    l = 2
    while l <= x:
        q = x // l
        r = x // q
        res -= (tri(r) - tri(l - 1)) * getA(q)
        l = r + 1
    AV[ii] = res

    res = tri(x)
    l = 2
    while l <= x:
        q = x // l
        r = x // q
        res -= (getM(r) - getM(l - 1)) * getF(q)
        l = r + 1
    FV[ii] = res

ans = 0
l = 1
while l <= N:
    q = N // l
    r = N // q
    coef = getA(r) - getA(l - 1)
    fv = getF(q) % MOD
    ans = (ans + (coef % MOD) * fv * fv) % MOD
    l = r + 1

print(ans)