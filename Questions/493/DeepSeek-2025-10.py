import math


def main():
    # Total balls: 70, balls per color: 10, colors: 7, sample size: 20

    # Compute log of combinations using logarithms for numerical stability
    # log(C(60, 20)) = log(60!) - log(20!) - log(40!)
    # log(C(70, 20)) = log(70!) - log(20!) - log(50!)

    # We can compute the ratio C(60,20)/C(70,20) using logarithms:
    # log_ratio = [log(60!) - log(20!) - log(40!)] - [log(70!) - log(20!) - log(50!)]
    # = log(60!) + log(50!) - log(70!) - log(40!)

    # Using math.lgamma(n+1) = log(n!)
    log_60_fact = math.lgamma(61)  # log(60!)
    log_50_fact = math.lgamma(51)  # log(50!)
    log_70_fact = math.lgamma(71)  # log(70!)
    log_40_fact = math.lgamma(41)  # log(40!)

    log_ratio = log_60_fact + log_50_fact - log_70_fact - log_40_fact
    ratio = math.exp(log_ratio)

    # Probability that a specific color appears
    prob_color_present = 1 - ratio

    # Expected number of distinct colors
    expected = 7 * prob_color_present

    # Format to 9 decimal places
    print(f"{expected:.9f}")


if __name__ == "__main__":
    main()