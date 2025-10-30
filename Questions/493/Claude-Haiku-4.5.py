#### iki kez sonucu kendi hesapladı. Israr edince kodu yazdı:
##### https://claude.ai/chat/6464c003-f82c-488f-aecb-692088735717
from math import comb

# Problem parameters
total_balls = 70
balls_per_color = 10
num_colors = 7
picks = 20

# For each color, calculate the probability it appears in our sample
# P(color does NOT appear) = C(60, 20) / C(70, 20)
# This is: choose 20 balls from the 60 non-matching balls / choose 20 from all 70

prob_not_appearing = comb(total_balls - balls_per_color, picks) / comb(total_balls, picks)

# P(color appears) = 1 - P(color does not appear)
prob_appearing = 1 - prob_not_appearing

# Expected number of distinct colors (by linearity of expectation)
# Sum over all 7 colors: P(color appears)
expected_distinct_colors = num_colors * prob_appearing

print(f"{expected_distinct_colors:.9f}")