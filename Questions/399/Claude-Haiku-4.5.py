def sieve_of_eratosthenes(limit):
    """Generate primes up to limit"""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

    return [i for i in range(2, limit + 1) if is_prime[i]]


# Generate small primes - 200K primes covers p^2 checks effectively
primes = sieve_of_eratosthenes(200_000)
# Pre-compute squares for faster checking
prime_squares = [p * p for p in primes]


def is_squarefree(n):
    """Check if n is squarefree by testing divisibility by p^2"""
    if n <= 1:
        return True

    # Check divisibility by p^2 for each small prime
    for p_sq in prime_squares:
        if p_sq > n:
            break
        if n % p_sq == 0:
            return False

    return True


# Initialize Fibonacci sequence
count = 0
a, b = 1, 1

# Check first Fibonacci number
if is_squarefree(a):
    count += 1

# Generate Fibonacci numbers until we reach the target
target = 100_000_000
while count < target:
    a, b = b, a + b
    if is_squarefree(b):
        count += 1

result = b

# Extract last 16 digits
last_16_digits = result % (10 ** 16)

# Compute scientific notation
result_str = str(result)
exponent = len(result_str) - 1

# Get mantissa to 1 decimal place
if len(result_str) > 1:
    mantissa = float(result_str[0] + '.' + result_str[1])
else:
    mantissa = float(result_str[0])

sci_notation = f"{mantissa:.1f}e{exponent}"

# Output in required format: last 16 digits, comma, scientific notation
print(f"{last_16_digits:016d},{sci_notation}")