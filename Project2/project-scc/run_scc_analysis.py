import random
from pprint import pprint
from time import time
from typing import Callable

from graphs import generate_graph
# noinspection PyUnusedImports
from scc import prepost, find_sccs


def generate_and_analyze_graph(
        seed: int,
        n: int,
        density_factor: float,
        analyze: Callable
) -> tuple[int, int, float]:
    random.seed(seed)
    graph = generate_graph(n, density_factor)

    V = len(graph)
    E = sum(len(edges) for edges in graph.values())

    start = time()

    analyze(graph)

    duration = time() - start

    return V, E, duration


def _compute_average_runtimes(runtimes):
    groups = {}
    for dens, size, v, e, runtime in runtimes:
        key = (dens, size)
        if key not in groups:
            groups[key] = []
        groups[key].append((v, e, runtime))

    return [
        (
            dens,
            size,
            round(sum(v for v, _, _ in stats) / len(stats), 3),
            round(sum(e for _, e, _ in stats) / len(stats), 3),
            round(sum(t for _, _, t in stats) / len(stats), 3)
        )
        for (dens, size), stats in groups.items()
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

    print('Copy this markdown table into your report:')
    print()
    print('\n'.join(rows))


def main():
    densities = [0.25, 0.5, 1, 2, 3]
    sizes = [10, 50, 100, 500, 1000, 2000, 4000, 8000]

    runtimes = []
    for density_factor in densities:
        print('Running with density factor', density_factor)
        for size in sizes:
            print('Running with size', size)
            for iteration in range(10):
                v, e, runtime = generate_and_analyze_graph(
                    225 + iteration,
                    size,
                    density_factor,
                    # Pass in either prepost
                    prepost,
                    # or find_sccs
                    # find_sccs
                    # for the analysis you want to run on the graph
                )
                runtimes.append((density_factor, size, v, e, runtime))

    ave_runtimes = _compute_average_runtimes(runtimes)

    print()
    _print_markdown_table(
        ave_runtimes,
        ['Density Factor', 'Size ', '   V   ', '   E   ', 'Time (sec)']
    )

    # Print runtimes to a file
    with open('_runtimes.py', 'w') as file:
        print('runtimes = ', end='', file=file)
        pprint(runtimes, file)

    print()
    print('_runtimes.py written')


if __name__ == '__main__':
    main()
