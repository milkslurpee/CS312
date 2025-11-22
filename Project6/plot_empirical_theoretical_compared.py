import matplotlib.pyplot as plt
import numpy as np
from _runtimes import runtimes
import math

def main():
    # Theoretical time complexity: O(n log n)
    def theoretical_big_o(n):
        return n*n*n

    # Coefficient from your analysis
    coeff = 1.6253781284970658e-07

    n_values = [n for n, _, _ in runtimes]
    times = [t for _,_, t in runtimes]

    # Compute theoretical prediction
    predicted_runtime = [coeff * theoretical_big_o(n) for n in n_values]

    # Plot observed runtimes
    plt.scatter(n_values, times, color='blue', label='Observed', zorder=3)

    # Plot theoretical curve
    plt.plot(n_values, predicted_runtime, color='red', linestyle='--', label='Theoretical (n^3)', zorder=2)

    # Axis labels and title
    plt.xlabel('Number of Cities (N)')
    plt.ylabel('Time (ms)')
    plt.title('Greedy: Empirical vs. Theoretical Runtime')
    plt.legend()
    plt.grid(True)

    # Save figure
    plt.savefig('_analysis/greedy.svg')
    plt.show()

if __name__ == '__main__':
    main()
