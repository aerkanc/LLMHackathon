import math

def main():
    max_index = -1
    max_value = -1.0

    with open("./0099_base_exp.txt", "r") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            base_str, exp_str = line.split(',')
            base = int(base_str)
            exp = int(exp_str)
            # Compare using logarithms: log(a^b) = b * log(a)
            val = exp * math.log(base)
            if val > max_value:
                max_value = val
                max_index = idx

    print(max_index)

if __name__ == "__main__":
    main()