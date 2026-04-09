import math
from pathlib import Path

def find_input_file():
    candidates = [
        Path("base_exp.txt"),
        Path("./099_base_exp.txt"),
        Path("/mnt/data/base_exp.txt"),
        Path("/mnt/data/p099_base_exp.txt"),
    ]
    for path in candidates:
        if path.is_file():
            return path
    for path in Path(".").rglob("*.txt"):
        try:
            with path.open("r", encoding="utf-8") as f:
                first = f.readline().strip()
                if "," in first:
                    a, b = first.split(",")
                    int(a)
                    int(b)
                    return path
        except Exception:
            pass
    raise FileNotFoundError("Input file not found")

best_line = 0
best_value = float("-inf")

with find_input_file().open("r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        base, exp = map(int, line.strip().split(","))
        value = exp * math.log(base)
        if value > best_value:
            best_value = value
            best_line = i

print(best_line)