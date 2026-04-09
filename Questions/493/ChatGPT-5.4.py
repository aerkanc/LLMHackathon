from math import comb

total_balls = 70
balls_per_colour = 10
num_colours = 7
draws = 20

p_missing_one_colour = comb(total_balls - balls_per_colour, draws) / comb(total_balls, draws)
expected_distinct_colours = num_colours * (1 - p_missing_one_colour)

print(f"{expected_distinct_colours:.9f}")