import time
import random
import matplotlib.pyplot as plt
import numpy as np
from prime_number_generation import generate_large_prime

import sys
sys.setrecursionlimit(10000)

# Copy your mod_exp and fermat functions here
def mod_exp(x: int, y: int, N: int) -> int:
    if y == 0: return 1
    z = mod_exp(x, y // 2, N)
    if y % 2 == 0: return (z ** 2) % N
    else: return (x * (z ** 2)) % N

def fermat(N: int, k: int) -> bool:
    if N == 2 or N == 3: return True
    if N <= 1 or N % 2 == 0 or N % 3 == 0: return False
    for j in range(1, k + 1):
        a = random.randint(1, N - 1)
        if mod_exp(a, N - 1, N) != 1: return False
    return True

def generate_large_prime(n_bits: int) -> int:
    num = random.getrandbits(n_bits)
    if fermat(num, 20) == False:
        return generate_large_prime(n_bits)
    else: return num


# --------------------------
# Measure runtime for different bit lengths
# --------------------------
bit_lengths = [64, 128, 256, 512, 1024, 2048]
runtimes = []

for bits in bit_lengths:
    print(f"Generating prime with {bits} bits...", end=' ')
    start = time.time()
    generate_large_prime(bits)
    end = time.time()
    runtime = end - start
    runtimes.append(runtime)
    print(f"took {runtime:.4f} seconds")

# --------------------------
# Plot Observed Runtime
# --------------------------
plt.plot(bit_lengths, runtimes, marker='o', linestyle='-', label='Observed runtime')

# --------------------------
# Plot Theoretical Runtime: O(k·n⁴) where k=20
# --------------------------
k = 20  # from fermat(N, 20)
theoretical = [k * n**4 for n in bit_lengths]

# Scale to first observed runtime
scale = runtimes[0] / theoretical[0]
theoretical_scaled = [t * scale for t in theoretical]

plt.plot(bit_lengths, theoretical_scaled, marker='x', label='O(k·n⁴) estimate (k=20)', linestyle=':')

# --------------------------
# Empirical order of growth (slope in log-log space)
# --------------------------
log_n = np.log(bit_lengths)
log_t = np.log(runtimes)
slope, log_C = np.polyfit(log_n, log_t, 1)
C_empirical = np.exp(log_C)

# Generate empirical line
empirical_line = [C_empirical * n**slope for n in bit_lengths]
plt.plot(bit_lengths, empirical_line, marker='^', label=f'Empirical fit: n^{slope:.2f}', linestyle='--')

# --------------------------
# Final plot formatting
# --------------------------
plt.xlabel("Bit length (n_bits)")
plt.ylabel("Time (seconds)")
plt.title("Prime Generation Runtime vs Bit Length")
plt.legend()
plt.grid(True)
plt.yscale('log')  # Add log scale to better see the growth
plt.xscale('log')
plt.show()

print(f"Empirical order of growth (slope): {slope:.2f}")
print(f"Empirical constant of proportionality: {C_empirical:.6f}")
print(f"Theoretical slope expected: 4.00")