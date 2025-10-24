import matplotlib.pyplot as plt
import numpy as np
from _runtimes import runtimes

def main():
    # Theoretical time complexity: O(n log n)
    def theoretical_big_o(n):
        return (n * np.log(n)) / 12000

    # Coefficient from your analysis
    coeff = 0.00400676965713501

    n_values = [n for n, _ in runtimes]
    times = [t for _, t in runtimes]

    # Compute theoretical prediction
    predicted_runtime = [coeff * theoretical_big_o(n) for n in n_values]

    # Plot observed runtimes
    plt.scatter(n_values, times, color='blue', label='Observed', zorder=3)

    # Plot theoretical curve
    plt.plot(n_values, predicted_runtime, color='red', linestyle='--', label='Theoretical n log n', zorder=2)

    # Axis labels and title
    plt.xlabel('Number of Points (N)')
    plt.ylabel('Time (sec)')
    plt.title('Convex Hull: Empirical vs. Theoretical Runtime')
    plt.legend()
    plt.grid(True)

    # Save figure
    plt.savefig('_analysis/empirical_convex_hull.svg')
    plt.show()

if __name__ == '__main__':
    main()
