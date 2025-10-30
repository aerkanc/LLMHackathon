import math
import os

def find_file():
    # Try common locations
    candidates = [
        "base_exp.txt",
        os.path.join(os.getcwd(), "base_exp.txt"),
        os.path.join(os.path.dirname(__file__), "base_exp.txt") if "__file__" in globals() else None,
        "/mnt/data/base_exp.txt",
    ]
    for p in candidates:
        if p and os.path.isfile(p):
            return p
    raise FileNotFoundError("base_exp.txt not found in expected locations.")

def main():
    path = find_file()
    max_val = float("-inf")
    max_idx = -1
    with open(path, "r") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            b_str, e_str = line.split(",")
            b = int(b_str)
            e = int(e_str)
            # Compare by logarithms: b^e vs c^d -> e*ln(b) vs d*ln(c)
            val = e * math.log(b)
            if val > max_val:
                max_val = val
                max_idx = i
    print(max_idx)

if __name__ == "__main__":
    main()
