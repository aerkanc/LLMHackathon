import multiprocessing as mp

# Precomputed squares of digits 0-9
SQ = [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

def next_sum(n: int) -> int:
    """Return sum of squares of digits of n."""
    s = 0
    while n:
        n, d = divmod(n, 10)
        s += SQ[d]
    return s

def precompute_ends(limit: int = 568):
    """Compute final outcome (1 or 89) for all numbers < limit."""
    end = [0] * limit          # 0 means unknown
    end[1] = 1
    end[89] = 89
    for i in range(1, limit):
        if end[i] != 0:
            continue
        # Follow the chain until we hit a known value
        chain = []
        cur = i
        while end[cur] == 0:
            chain.append(cur)
            cur = next_sum(cur)
            # cur is guaranteed to be < limit because for any n < 568,
            # next_sum(n) <= 9*9*3 = 243 < 568
        res = end[cur]
        for x in chain:
            end[x] = res
    return end

def count_chunk(start: int, stop: int, end_lookup):
    """Count numbers in [start, stop) that end at 89."""
    cnt = 0
    for n in range(start, stop):
        if end_lookup[next_sum(n)] == 89:
            cnt += 1
    return cnt

def main():
    # Precompute outcomes for numbers 0..567 (568 entries)
    end = precompute_ends(568)

    # Total numbers to consider: 1 .. 9,999,999
    N = 10_000_000
    # Use all available CPU cores
    num_workers = mp.cpu_count()
    # Compute chunk boundaries
    chunk_size = (N + num_workers - 1) // num_workers
    chunks = []
    for start in range(1, N, chunk_size):
        stop = min(start + chunk_size, N)
        chunks.append((start, stop, end))

    # Parallel counting
    with mp.Pool(processes=num_workers) as pool:
        results = pool.starmap(count_chunk, chunks)

    total = sum(results)
    print(total)

if __name__ == "__main__":
    main()