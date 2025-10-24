import math
import random
from pprint import pprint
from time import time
from typing import Callable

# noinspection PyUnusedImports
from main import find_shortest_path_with_heap, find_shortest_path_with_linear_pq
from main import generate_graph


def generate_and_analyze_graph(
        seed: int,
        size: int,
        density: float,
        noise: float,
        distribution: str,
        analyze: Callable
) -> tuple[int, int, float]:
    random.seed(seed)
    points, graph = generate_graph(seed, size, density, noise, distribution)

    V = len(graph)
    E = sum(
        sum(
            not math.isinf(edge_weight)
            for edge_weight in edges.values()
        )
        for edges in graph.values()
    )

    sorted_points = list(sorted(
        range(len(points)),
        key=lambda pos: (points[pos][0]**2 + points[pos][1]**2)**0.5
    ))

    source = sorted_points[0]
    target = sorted_points[-1]

    start = time()

    analyze(graph, source, target)

    duration = time() - start

    return V, E, duration


def _compute_average_runtimes(runtimes):
    groups = {}
    for v, e, runtime in runtimes:
        key = v
        if key not in groups:
            groups[key] = []
        groups[key].append((v, e, runtime))

    return [
        (
            size,
            round(sum(e for _, e, _ in stats) / len(stats), 3),
            round(sum(t for _, _, t in stats) / len(stats), 3)
        )
        for size, stats in groups.items()
    ]


def _print_markdown_table(ave_runtimes, headers):
    header_widths = [len(header) for header in headers]

    rows = [
        '| ' + ' | '.join(headers) + ' |',
        '| ' + ' | '.join('-' * len(header) for header in headers) + ' |'
    ]

    rows += (
        '| ' + ' | '.join(
            f'{field:<{width}}'
            for field, width in zip(row, header_widths)
        ) + ' |'
        for row in ave_runtimes
    )

    print('\n'.join(rows))


def main():
    distribution = 'uniform'
    density = 0.3
    noise = 0.05
    sizes = [500, 1000, 1500, 2000, 2500, 3000, 3500]

    # pq_algorithm = 'Linear'
    # algorithm = find_shortest_path_with_linear_pq

    pq_algorithm = 'Heap'
    algorithm = find_shortest_path_with_heap

    runtimes = []
    for size in sizes:
        print('Running with size', size)
        for iteration in range(10):
            v, e, runtime = generate_and_analyze_graph(
                225 + iteration,
                size,
                density,
                noise,
                distribution,
                algorithm
            )
            runtimes.append((v, e, runtime))

    ave_runtimes = _compute_average_runtimes(runtimes)

    print()
    print('Copy this markdown table into your report:  ')
    print()

    print(f'Distribution: **{distribution}**  ')
    print(f'Density: **{density}**  ')
    print(f'Noise: **{noise}**  ')
    print(f'PQ Implementation: **{pq_algorithm}**  ')

    print()
    _print_markdown_table(
        ave_runtimes,
        ['   V   ', '   E   ', 'Time (sec)']
    )

    # Print runtimes to a file
    with open('_runtimes.py', 'w') as file:
        print(f'distribution = {repr(distribution)}', file=file)
        print(f'density = {density}', file=file)
        print(f'noise = {noise}', file=file)
        print(f'pq_algorithm = {repr(pq_algorithm)}', file=file)

        print('runtimes = ', end='', file=file)
        pprint(runtimes, file)

    print()
    print('_runtimes.py written')


if __name__ == '__main__':
    main()
