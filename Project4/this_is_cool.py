#!/usr/bin/env python3
"""
test_hull_plot.py
-----------------
Generates a large, irregular random point cloud (non-square),
computes the convex hull using compute_hull_dvcq(),
and visualizes it.
"""

import random
import math
import matplotlib.pyplot as plt
from main import compute_hull_dvcq  # adjust if your main file has a different name


# Number of total points to generate
NUM_POINTS = 10000  # Try 50000+ for a bigger challenge
NUM_CLUSTERS = 1    # How many clusters to scatter around

def generate_irregular_points(n, clusters=5):
    """Generate n points distributed in random, non-square clusters."""
    points = []
    for _ in range(clusters):
        # Random cluster center (spread across a wide irregular region)
        cx = random.uniform(-2000, 2000)
        cy = random.uniform(-1000, 3000)

        # Each cluster can be stretched differently
        stretch_x = random.uniform(100, 800)
        stretch_y = random.uniform(100, 1200)
        angle = random.uniform(0, 2 * math.pi)

        # Rotation matrix for cluster orientation
        cos_a, sin_a = math.cos(angle), math.sin(angle)

        for _ in range(n // clusters):
            # Elliptical cluster point
            rx = random.gauss(0, stretch_x)
            ry = random.gauss(0, stretch_y)
            # Apply rotation
            x = cx + rx * cos_a - ry * sin_a
            y = cy + rx * sin_a + ry * cos_a
            points.append((x, y))

    random.shuffle(points)
    return points


def plot_points_and_hull(points, hull):
    """Display scatter plot of points and overlay convex hull."""
    xs, ys = zip(*points)
    plt.figure(figsize=(12, 8))
    plt.scatter(xs, ys, s=5, alpha=0.4, label="Points", color="gray")

    if hull:
        hx, hy = zip(*(hull + [hull[0]]))  # close the hull
        plt.plot(hx, hy, "r-", linewidth=2, label="Convex Hull")

    plt.title(f"Convex Hull of {len(points):,} Randomly Distributed Points")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


def main():
    print(f"Generating {NUM_POINTS:,} random, irregularly distributed points...")
    points = generate_irregular_points(NUM_POINTS, clusters=NUM_CLUSTERS)

    print("Computing convex hull using divide-and-conquer algorithm...")
    hull = compute_hull_dvcq(points)

    print(f"Convex hull computed with {len(hull)} vertices.")
    plot_points_and_hull(points, hull)


if __name__ == "__main__":
    main()
