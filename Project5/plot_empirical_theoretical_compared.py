import matplotlib.pyplot as plt
import numpy as np
from _runtimes import runtimes  # expects runtimes = [(N, time_in_seconds), ...]

def main():
    # --- Extract empirical data ---
    sizes = np.array([n for n, _ in runtimes])
    times = np.array([t for _, t in runtimes])

    # --- Sort by sequence size just in case ---
    order = np.argsort(sizes)
    sizes = sizes[order]
    times = times[order]

    # --- Convert seconds → milliseconds for readability ---
    times_ms = times * 1000

    # --- Define theoretical model ---
    # Needleman–Wunsch is O(N^2), so use N^2 scaling
    def theoretical_big_o(n):
        return (n ** 2)  # arbitrary scaling for shape; will fit coefficient next

    # Fit coefficient empirically to match rough magnitude
    coeff = 5.825482232835558e-07

    # Compute predicted times
    predicted = coeff * theoretical_big_o(sizes)

    # --- Plot results ---
    plt.figure(figsize=(8, 6))
    plt.plot(sizes, times_ms, 'o-', label='Observed Runtime')
    plt.plot(sizes, predicted, 'k--', label=f'Theoretical ~ {coeff:.2e} * O(N²)')
    plt.xlabel('Sequence Length (N)')
    plt.ylabel('Runtime (ms)')
    plt.title('Needleman–Wunsch Runtime Analysis')
    plt.legend()
    plt.grid(True, linestyle=':')
    plt.tight_layout()

    # Save and show
    plt.savefig('NW_analysis_runtime.svg', format='svg')
    plt.show()

    print(f"Fitted coefficient: {coeff:.6e}")

if __name__ == '__main__':
    main()
