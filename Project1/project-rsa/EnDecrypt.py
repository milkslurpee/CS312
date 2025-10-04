import time
import sys
import matplotlib.pyplot as plt
import numpy as np
from generate_keypair import generate_key_pairs
from prime_number_generation import mod_exp

sys.setrecursionlimit(10000)


def empirical_encrypt_decrypt_analysis(bit_lengths=[64, 128, 256, 512, 1024, 2048]):
    """
    Run empirical analysis of RSA encryption and decryption for different bit sizes.
    """
    encrypt_times = []
    decrypt_times = []
    successful_runs = []

    print("=== RSA Encryption/Decryption Empirical Analysis ===")

    for bits in bit_lengths:
        print(f"Testing {bits} bits...", end=' ')
        start_keygen = time.time()
        try:
            # Generate key pair first
            N, e, d = generate_key_pairs(bits)
            keygen_time = time.time() - start_keygen

            # Test message for encryption/decryption
            test_message = 42  # Small test message

            # Measure encryption time
            encrypt_start = time.time()
            encrypted = mod_exp(test_message, e, N)
            encrypt_time = (time.time() - encrypt_start) * 1000  # Convert to ms
            encrypt_times.append(encrypt_time)

            # Measure decryption time
            decrypt_start = time.time()
            decrypted = mod_exp(encrypted, d, N)
            decrypt_time = (time.time() - decrypt_start) * 1000  # Convert to ms
            decrypt_times.append(decrypt_time)

            # Verify correctness
            verification = "✓" if test_message == decrypted else "✗"
            successful_runs.append(True)

            print(f"Encrypt: {encrypt_time:.3f}ms, Decrypt: {decrypt_time:.3f}ms {verification}")

        except Exception as e:
            print(f"ERROR: {e}")
            encrypt_times.append(None)
            decrypt_times.append(None)
            successful_runs.append(False)
            continue

    # Filter successful runs
    valid_bits = [bit_lengths[i] for i in range(len(bit_lengths)) if successful_runs[i]]
    valid_encrypt = [encrypt_times[i] for i in range(len(encrypt_times)) if successful_runs[i]]
    valid_decrypt = [decrypt_times[i] for i in range(len(decrypt_times)) if successful_runs[i]]

    if not valid_encrypt:
        print("No successful runs to plot")
        return

    # Create plots
    plt.figure(figsize=(15, 10))

    # Plot 1: Linear scale
    plt.subplot(2, 2, 1)
    plt.plot(valid_bits, valid_encrypt, 'bo-', label='Encryption', linewidth=2, markersize=6)
    plt.plot(valid_bits, valid_decrypt, 'ro-', label='Decryption', linewidth=2, markersize=6)
    plt.xlabel("Bit length")
    plt.ylabel("Time (ms)")
    plt.title("RSA Encryption/Decryption Time (Linear)")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 2: Log-log scale
    plt.subplot(2, 2, 2)
    plt.loglog(valid_bits, valid_encrypt, 'bo-', label='Encryption', linewidth=2, markersize=6)
    plt.loglog(valid_bits, valid_decrypt, 'ro-', label='Decryption', linewidth=2, markersize=6)
    plt.xlabel("Bit length")
    plt.ylabel("Time (ms)")
    plt.title("RSA Encryption/Decryption Time (Log-Log)")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 3: Theoretical vs Empirical fits
    plt.subplot(2, 2, 3)

    # Plot empirical data
    plt.plot(valid_bits, valid_encrypt, 'bo-', label='Encryption Empirical', linewidth=2, markersize=6)
    plt.plot(valid_bits, valid_decrypt, 'ro-', label='Decryption Empirical', linewidth=2, markersize=6)

    # Fit empirical curves and plot
    if len(valid_bits) >= 2:
        # Encryption fit
        log_bits_encrypt = np.log(valid_bits)
        log_time_encrypt = np.log(valid_encrypt)
        slope_encrypt, intercept_encrypt = np.polyfit(log_bits_encrypt, log_time_encrypt, 1)
        C_encrypt = np.exp(intercept_encrypt)
        encrypt_fit = [C_encrypt * n ** slope_encrypt for n in valid_bits]
        plt.plot(valid_bits, encrypt_fit, 'b:', label=f'Encrypt Fit: O(n^{slope_encrypt:.2f})', linewidth=2)

        # Decryption fit
        log_bits_decrypt = np.log(valid_bits)
        log_time_decrypt = np.log(valid_decrypt)
        slope_decrypt, intercept_decrypt = np.polyfit(log_bits_decrypt, log_time_decrypt, 1)
        C_decrypt = np.exp(intercept_decrypt)
        decrypt_fit = [C_decrypt * n ** slope_decrypt for n in valid_bits]
        plt.plot(valid_bits, decrypt_fit, 'r:', label=f'Decrypt Fit: O(n^{slope_decrypt:.2f})', linewidth=2)

    plt.xlabel("Bit length")
    plt.ylabel("Time (ms)")
    plt.title("Theoretical vs Empirical Fits")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    plt.xscale('log')

    # Plot 4: Ratio of decrypt/encrypt times
    plt.subplot(2, 2, 4)
    ratios = [decrypt / encrypt for encrypt, decrypt in zip(valid_encrypt, valid_decrypt)]
    plt.plot(valid_bits, ratios, 'go-', label='Decrypt/Encrypt Ratio', linewidth=2, markersize=6)
    plt.xlabel("Bit length")
    plt.ylabel("Time Ratio")
    plt.title("Decryption vs Encryption Time Ratio")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('rsa_encrypt_decrypt_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Print results table
    print(f"\n### Empirical Data")
    print()
    print("| N (bits) | Encrypt (ms) | Decrypt (ms) | Ratio |")
    print("|----------|--------------|--------------|-------|")
    for i, bits in enumerate(bit_lengths):
        if i < len(encrypt_times) and encrypt_times[i] is not None:
            ratio = decrypt_times[i] / encrypt_times[i] if encrypt_times[i] > 0 else float('inf')
            print(f"| {bits}      | {encrypt_times[i]:.3f}       | {decrypt_times[i]:.3f}       | {ratio:.1f}  |")
        else:
            print(f"| {bits}      | Failed       | Failed       | -     |")

    # Print analysis results
    if len(valid_bits) >= 2:
        print(f"\n### Analysis Results")
        print(f"ENCRYPTION:")
        print(f"  Theoretical order of growth: O(n³)")
        print(f"  Empirical order of growth: O(n^{slope_encrypt:.2f})")
        print(f"  Empirical constant: {C_encrypt:.6e} ms/bit^{slope_encrypt:.2f}")

        print(f"\nDECRYPTION:")
        print(f"  Theoretical order of growth: O(n³)")
        print(f"  Empirical order of growth: O(n^{slope_decrypt:.2f})")
        print(f"  Empirical constant: {C_decrypt:.6e} ms/bit^{slope_decrypt:.2f}")

        print(f"\nCOMPARISON:")
        print(f"  Average decrypt/encrypt ratio: {np.mean(ratios):.1f}x")
        print(f"  Encryption vs theoretical difference: {3 - slope_encrypt:.2f} orders")
        print(f"  Decryption vs theoretical difference: {3 - slope_decrypt:.2f} orders")

    return {
        'bit_lengths': valid_bits,
        'encrypt_times': valid_encrypt,
        'decrypt_times': valid_decrypt,
        'encrypt_slope': slope_encrypt if len(valid_bits) >= 2 else None,
        'decrypt_slope': slope_decrypt if len(valid_bits) >= 2 else None,
        'encrypt_constant': C_encrypt if len(valid_bits) >= 2 else None,
        'decrypt_constant': C_decrypt if len(valid_bits) >= 2 else None
    }


# Quick test function for smaller bit sizes
def quick_test():
    """Quick test with smaller bit sizes"""
    return empirical_encrypt_decrypt_analysis([64, 128, 256, 512])


if __name__ == "__main__":
    # Run the full analysis
    results = empirical_encrypt_decrypt_analysis([64, 128, 256, 512, 1024, 2048])

    # If that's too slow, run quick test instead
    # results = quick_test()