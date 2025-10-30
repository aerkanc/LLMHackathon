import math

max_log_value = float('-inf')
max_line_number = -1

with open('base_exp.txt', 'r') as f:
    for line_number, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue

        try:
            base, exponent = map(int, line.split(','))
        except (ValueError, IndexError):
            continue

        # Use logarithms to compare: log(base^exponent) = exponent * log(base)
        # This avoids computing the massive numbers directly
        log_value = exponent * math.log(base)

        if log_value > max_log_value:
            max_log_value = log_value
            max_line_number = line_number

print(max_line_number)