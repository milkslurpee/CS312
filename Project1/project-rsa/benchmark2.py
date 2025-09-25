import time
import sys
import matplotlib.pyplot as plt
import numpy as np
from generate_keypair import generate_key_pairs
from prime_number_generation import mod_exp

sys.setrecursionlimit(10000)


def empirical_analysis(bit_lengths=[64, 128, 256, 512, 1024, 2048]):
    """
    Run empirical analysis of generate_key_pairs for different bit sizes.
    Simplified version that matches the prime generation analysis style.

    Args:
        bit_lengths: List of bit sizes to test

    Returns:
        Dictionary with timing results
    """

    runtimes = []
    successful_keys = []

    print("=== RSA Key Generation Empirical Analysis ===")

    for bits in bit_lengths:
        print(f"Generating RSA keys with {bits} bits...", end=' ')
        start = time.time()
        try:
            N, e, d = generate_key_pairs(bits)
            end = time.time()
            runtime = end - start
            runtimes.append(runtime)
            successful_keys.append(True)

            # Verify the keys work
            test_message = 42
            encrypted = mod_exp(test_message, e, N)
            decrypted = mod_exp(encrypted, d, N)
            verification = "✓" if test_message == decrypted else "✗"

            print(f"took {runtime:.4f} seconds {verification}")

        except Exception as e:
            print(f"ERROR: {e}")
            runtimes.append(None)
            successful_keys.append(False)
            continue

    # --------------------------
    # Plot Observed Runtime
    # --------------------------
    valid_bit_lengths = [bit_lengths[i] for i in range(len(bit_lengths)) if successful_keys[i]]
    valid_runtimes = [runtimes[i] for i in range(len(runtimes)) if successful_keys[i]]

    if not valid_runtimes:
        print("No successful key generations to plot")
        return

    plt.figure(figsize=(10, 6))
    plt.plot(valid_bit_lengths, valid_runtimes, marker='o', linestyle='-',
             label='Observed runtime', linewidth=2, markersize=8)

    # --------------------------
    # Plot Theoretical Runtime: O(n³) for RSA key generation
    # --------------------------
    # RSA key generation involves O(n³) operations for modular exponentiation
    theoretical = [n ** 3 for n in valid_bit_lengths]

    # Scale to first observed runtime
    if valid_runtimes:
        scale = valid_runtimes[0] / theoretical[0]
        theoretical_scaled = [t * scale for t in theoretical]

        plt.plot(valid_bit_lengths, theoretical_scaled, marker='x',
                 label='O(n³) theoretical estimate', linestyle=':', linewidth=2, markersize=8)

    # --------------------------
    # Empirical order of growth (slope in log-log space)
    # --------------------------
    if len(valid_bit_lengths) >= 2:
        log_n = np.log(valid_bit_lengths)
        log_t = np.log(valid_runtimes)
        slope, log_C = np.polyfit(log_n, log_t, 1)
        C_empirical = np.exp(log_C)

        # Generate empirical line
        empirical_line = [C_empirical * n ** slope for n in valid_bit_lengths]
        plt.plot(valid_bit_lengths, empirical_line, marker='^',
                 label=f'Empirical fit: n^{slope:.2f}', linestyle='--', linewidth=2, markersize=8)

    # --------------------------
    # Final plot formatting
    # --------------------------
    plt.xlabel("Bit length (n_bits)")
    plt.ylabel("Time (seconds)")
    plt.title("RSA Key Generation Runtime vs Bit Length")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    plt.xscale('log')
    plt.tight_layout()
    plt.savefig('rsa_keygen_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Print results
    print(f"\n### Empirical Data")
    print()
    print("| N (bits) | time (seconds) |")
    print("|----------|----------------|")
    for i, bits in enumerate(bit_lengths):
        if i < len(runtimes) and runtimes[i] is not None:
            print(f"| {bits}      | {runtimes[i]:.4f}        |")
        else:
            print(f"| {bits}      | Failed         |")

    if len(valid_bit_lengths) >= 2:
        print(f"\nEmpirical order of growth (slope): {slope:.2f}")
        print(f"Empirical constant of proportionality: {C_empirical:.6f}")
        print(f"Theoretical slope expected: 3.00")

    return {
        'bit_lengths': bit_lengths,
        'runtimes': runtimes,
        'successful': successful_keys,
        'slope': slope if len(valid_bit_lengths) >= 2 else None,
        'constant': C_empirical if len(valid_bit_lengths) >= 2 else None
    }


# Alternative: Single trial with verification
def quick_analysis(bit_lengths=[64, 128, 256, 512]):
    """Quick analysis for smaller bit sizes"""
    return empirical_analysis(bit_lengths)


# Usage example:
if __name__ == "__main__":
    # Run the analysis
    results = empirical_analysis(
        bit_lengths=[64, 128, 256, 512, 1024, 2048]
    )