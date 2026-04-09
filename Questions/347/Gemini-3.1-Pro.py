import numpy as np
from concurrent.futures import ProcessPoolExecutor
import math

# Global değişkenler (Linux fork mekanizması ile child process'lere kopyalanmadan aktarılır)
N = 10000000
primes = None


def get_primes(limit):
    """NumPy kullanarak limit değerine kadar olan asalları hızlıca bulur."""
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0:2] = False
    for i in range(2, int(math.isqrt(limit)) + 1):
        if sieve[i]:
            sieve[i * i: limit + 1: i] = False
    return np.where(sieve)[0]


def worker_task(i):
    """
    Belirli bir p asalı (primes[i]) için tüm geçerli q asallarını dolaşıp
    M(p, q, N) değerlerini hesaplar.
    """
    local_m_values = set()
    p = int(primes[i])

    # p * q <= N koşulundan dolayı q'nun maksimum değeri N // p olabilir.
    max_q = N // p

    j = i + 1
    num_primes = len(primes)

    while j < num_primes:
        q = int(primes[j])
        if q > max_q:
            break

        # M(p, q, N) değerini bul: p^a * q^b <= N şartını sağlayan en büyük değer
        max_val = 0
        pa = p
        while pa * q <= N:
            curr = pa * q
            # q ile çarpmaya devam et
            while curr * q <= N:
                curr *= q

            if curr > max_val:
                max_val = curr

            # p'nin bir sonraki kuvvetine geç
            pa *= p

        if max_val > 0:
            local_m_values.add(max_val)

        j += 1

    return local_m_values


def solve():
    global primes

    # p * q <= N olduğu için en küçük asal 2'dir, en büyük asal limit N // 2 olur.
    limit = N // 2
    primes = get_primes(limit)

    # p asalının alabileceği maksimum değer isqrt(N)'dir (çünkü p < q).
    max_p = math.isqrt(N)

    # max_p değerine kadar kaç tane asal (p) olduğunu bulalım.
    num_p = 0
    for p in primes:
        if p > max_p:
            break
        num_p += 1

    all_m_values = set()

    # 16-Core CPU'yu tam kapasite kullanmak için ProcessPoolExecutor
    with ProcessPoolExecutor() as executor:
        # Sadece geçerli p indekslerini process pool'a gönderiyoruz
        results = executor.map(worker_task, range(num_p))

        for res_set in results:
            all_m_values.update(res_set)

    # Tüm farklı M(p, q, N) değerlerinin toplamını ekrana bas (hackathon kurallarına uygun olarak)
    print(sum(all_m_values))


if __name__ == '__main__':
    solve()