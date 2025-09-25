import sys
from pathlib import Path
from time import time
import tempfile
import os

# Add the path to your project files
sys.path.append(r'C:\Stuff\Homework\Fall2025\CS312\Project1\project-rsa')

from generate_keypair import generate_key_pairs
from encrypt_decrypt_files import read_key, chunks, add_len_header_and_pad, strip_len_header_and_unpad, transform


def benchmark_rsa_direct(bit_lengths=None):
    """
    Test encryption and decryption speeds using direct function calls.
    """
    if bit_lengths is None:
        bit_lengths = [64, 128, 256, 512, 1024, 2048]

    # Test message (smaller for faster testing)
    test_message = b"Hello, RSA Benchmark! This is a test message." * 10  # ~500 bytes

    results = {
        'encryption': {},
        'decryption': {}
    }

    for n_bits in bit_lengths:
        print(f"Testing {n_bits}-bit RSA...")

        try:
            # Generate key pair directly
            start_keygen = time()
            N, e, d = generate_key_pairs(n_bits)
            keygen_time = time() - start_keygen
            print(f"  Key generation: {keygen_time:.3f}s")

            # Calculate chunk sizes (similar to read_key function)
            n_bytes = (N.bit_length() + 7) // 8
            plain_bytes = (N.bit_length() - 1) // 8
            if plain_bytes <= 0:
                print(f"  ⚠ Plain bytes too small, skipping...")
                continue

            # Benchmark encryption
            encrypt_start = time()

            # Prepare data for encryption (add header and pad)
            prepared = add_len_header_and_pad(test_message, plain_bytes)

            # Encrypt using transform function
            encrypted = transform(
                prepared, N, e,
                in_chunk_bytes=plain_bytes,
                out_chunk_bytes=n_bytes
            )
            encrypt_time = time() - encrypt_start

            # Benchmark decryption
            decrypt_start = time()

            # Decrypt using transform function
            decrypted_blocks = transform(
                encrypted, N, d,
                in_chunk_bytes=n_bytes,
                out_chunk_bytes=plain_bytes
            )

            # Remove header and padding
            decrypted = strip_len_header_and_unpad(decrypted_blocks)
            decrypt_time = time() - decrypt_start

            # Verify correctness
            if decrypted == test_message:
                print(f"  ✓ Encrypt: {encrypt_time * 1000:.3f}ms, Decrypt: {decrypt_time * 1000:.3f}ms")

                results['encryption'][n_bits] = encrypt_time * 1000
                results['decryption'][n_bits] = decrypt_time * 1000
            else:
                print(f"  ✗ Decryption verification failed!")
                print(f"    Original: {len(test_message)} bytes")
                print(f"    Decrypted: {len(decrypted)} bytes")

        except Exception as e:
            print(f"  ✗ Error: {e}")
            import traceback
            traceback.print_exc()
            continue

    return results


def print_results_table(results):
    """Print results in a formatted table."""
    print("\n" + "=" * 60)
    print("RSA PERFORMANCE BENCHMARK RESULTS")
    print("=" * 60)
    print(f"{'N (bits)':<8} {'Encryption (ms)':<15} {'Decryption (ms)':<15}")
    print("-" * 40)

    bit_lengths = sorted(results['encryption'].keys())

    for n_bits in bit_lengths:
        enc_time = results['encryption'][n_bits]
        dec_time = results['decryption'][n_bits]
        print(f"{n_bits:<8} {enc_time:.3f}{'':<8} {dec_time:.3f}{'':<8}")


def calculate_growth_rates(results):
    """Calculate and print growth rates between different bit lengths."""
    print("\n" + "=" * 60)
    print("GROWTH RATE ANALYSIS")
    print("=" * 60)

    bit_lengths = sorted(results['encryption'].keys())

    if len(bit_lengths) < 2:
        print("Not enough data points for growth analysis")
        return

    print(f"{'Bits':<10} {'Encrypt (ms)':<12} {'Growth':<10} {'Decrypt (ms)':<12} {'Growth':<10}")
    print("-" * 60)

    prev_enc = None
    prev_dec = None

    for n_bits in bit_lengths:
        enc_time = results['encryption'][n_bits]
        dec_time = results['decryption'][n_bits]

        enc_growth = "—"
        dec_growth = "—"

        if prev_enc is not None:
            enc_growth = f"{enc_time / prev_enc:.2f}x"
            dec_growth = f"{dec_time / prev_dec:.2f}x"

        print(f"{n_bits:<10} {enc_time:<12.3f} {enc_growth:<10} {dec_time:<12.3f} {dec_growth:<10}")

        prev_enc = enc_time
        prev_dec = dec_time


def theoretical_analysis():
    """Print theoretical expectations for comparison."""
    print("\n" + "=" * 60)
    print("THEORETICAL EXPECTATIONS")
    print("=" * 60)
    print("RSA complexity: O(n³) for n-bit numbers")
    print("When N doubles (n → 2n):")
    print("  - Encryption should grow by ~2³ = 8x")
    print("  - Decryption should grow by ~2³ = 8x (similar factor)")
    print("In practice, due to implementation optimizations:")
    print("  - Encryption often shows ~4-6x growth")
    print("  - Decryption often shows ~6-8x growth")
    print("\nNote: Your results may vary based on:")
    print("  - Modular exponentiation implementation")
    print("  - Python optimizations")
    print("  - Hardware performance")


# Run the benchmark
if __name__ == "__main__":
    print("Starting RSA Performance Benchmark (Direct Method)")
    print("This may take a while for larger key sizes...")

    # Start with smaller sizes for testing
    test_sizes = [64, 128, 256, 512, 1024, 2048]  # Add 1024, 2048 later if desired

    results = benchmark_rsa_direct(test_sizes)

    if results['encryption']:
        print_results_table(results)
        calculate_growth_rates(results)
        theoretical_analysis()

        # Export to CSV format for your report
        print("\n" + "=" * 60)
        print("CSV FORMAT FOR YOUR REPORT")
        print("=" * 60)
        print("N,Encryption(ms),Decryption(ms)")
        for n_bits in sorted(results['encryption'].keys()):
            enc = results['encryption'][n_bits]
            dec = results['decryption'][n_bits]
            print(f"{n_bits},{enc:.6f},{dec:.6f}")
    else:
        print("No successful benchmarks completed.")