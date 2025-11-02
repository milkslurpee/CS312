import matplotlib.pyplot as plt
import numpy as np
from _runtimes import runtimes  # expects runtimes = [(N, time_in_seconds), ...]

def main():
    sizes = np.array([n for n, _ in runtimes])
    times = np.array([t for _, t in runtimes])

    # sort
    order = np.argsort(sizes)
    sizes = sizes[order]
    times = times[order]

    # seconds → ms


    # theoretical model ~ O(N²)
    def theoretical_big_o(n):
        return n ** 2

    # empirically fit coefficient
    coeff = 5.760248067025784e-07


    predicted_ms = coeff * theoretical_big_o(sizes)

    # plot
    plt.figure(figsize=(8, 6))
    plt.plot(sizes, times, 'o-', label='Observed Runtime')
    plt.plot(sizes, predicted_ms, 'k--', label=f'Theoretical ~ N²')
    plt.xlabel('Sequence Length (N)')
    plt.ylabel('Runtime (ms)')
    plt.title('Needleman–Wunsch Runtime Analysis')
    plt.legend()
    plt.grid(True, linestyle=':')
    plt.tight_layout()
    plt.savefig('NW_analysis_runtime.svg', format='svg')
    plt.show()

    print(f"Fitted coefficient: {coeff:.6e}")

if __name__ == '__main__':
    main()
