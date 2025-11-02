import random
from time import time
from typing import Callable
from pprint import pprint

from main import align  # assumes align() and helpers are defined in main.py


def generate_random_sequence(length: int, alphabet: str = "ACGT") -> str:
    """Generate a random sequence of a given length using the provided alphabet."""
    return ''.join(random.choice(alphabet) for _ in range(length))


def generate_and_analyze_alignment(
        seed: int,
        length: int,
        banded_width: int,
        align_func: Callable
) -> float:
    """Generate two random sequences, run alignment, and record runtime (seconds)."""
    random.seed(seed)
    seq1 = generate_random_sequence(length)
    seq2 = generate_random_sequence(length)

    start = time()
    align_func(seq1, seq2, banded_width=banded_width)
    duration = time() - start  # keep in seconds, not ms for output file
    return duration


def main():
    banded_width = -1  # -1 for full alignment

    if banded_width == 3:
        sequence_sizes = [500, 1000, 5000, 10000, 15000, 20000, 25000, 30000]
    else:
        sequence_sizes = [500, 1000, 1500, 2000, 2500, 3000]

    iterations = 5
    runtimes = []

    print("| N    | time (ms) |")
    print("|------|-----------|")

    for size in sequence_sizes:
        times = []
        for i in range(iterations):
            runtime_sec = generate_and_analyze_alignment(
                seed=100 + i,
                length=size,
                banded_width=banded_width,
                align_func=align
            )
            runtimes.append((size, runtime_sec))  # store (N, time in seconds)
            times.append(runtime_sec * 1000)  # convert to ms for printing

        avg_time_ms = round(sum(times) / len(times), 2)
        print(f"| {size:<4} | {avg_time_ms:<9} |")

    # Save results exactly like the provided example
    with open("_runtimes.py", "w") as f:
        f.write("runtimes = ")
        pprint(runtimes, stream=f)

    print("\nt_runtimes.py written successfully.")


if __name__ == "__main__":
    main()

