from byu_pytest_utils import tier

from scc import prepost, find_sccs, classify_edges

baseline = tier('baseline', 1)
core = tier('core', 2)
stretch1 = tier('stretch1', 3)

graph1 = {
    'a': 'ef',
    'b': 'a',
    'c': 'de',
    'd': 'hi',
    'e': 'd',
    'f': 'bc',
    'g': 'd',
    'h': 'i',
    'i': 'l',
    'j': 'fhk',
    'k': 'ij',
    'l': 'g'
}

graph2 = {
    'n01': ['n02'],
    'n02': ['n05'],
    'n03': ['n02'],
    'n04': ['n03', 'n05'],
    'n05': ['n04', 'n06'],
    'n06': ['n05', 'n07', 'n08'],
    'n07': ['n05', 'n06', 'n08'],
    'n08': ['n05', 'n06'],
    'n09': ['n07'],
    'n10': ['n08']
}


@baseline
def test_prepost():
    prepost_numbers = prepost(graph1)

    expected_prepost_numbers = [
        {
            'a': [1, 20],
            'e': [2, 13],
            'd': [3, 12],
            'h': [4, 11],
            'i': [5, 10],
            'l': [6, 9],
            'g': [7, 8],
            'f': [14, 19],
            'b': [15, 16],
            'c': [17, 18],
        },
        {
            'j': [21, 24],
            'k': [22, 23],
        }
    ]

    assert prepost_numbers == expected_prepost_numbers


@baseline
def test_prepost_2():
    expected_post_numbers = [
        {
            'n01': [1, 16],
            'n02': [2, 15],
            'n03': [5, 6],
            'n04': [4, 7],
            'n05': [3, 14],
            'n06': [8, 13],
            'n07': [9, 12],
            'n08': [10, 11],
        },
        {
            'n09': [17, 18],
        },
        {
            'n10': [19, 20],
        }
    ]

    post_numbers = prepost(graph2)
    assert post_numbers == expected_post_numbers


@core
def test_scc():
    expected_sccs = [
        {'d', 'g', 'l', 'i', 'h'},
        {'e'},
        {'c'},
        {'a', 'b', 'f'},
        {'j', 'k'}
    ]

    sccs = find_sccs(graph1)

    assert sccs == expected_sccs


@core
def test_scc_2():
    sccs = find_sccs(graph2)
    expected_sccs = [
        {'n02', 'n03', 'n04', 'n05', 'n06', 'n07', 'n08'},
        {'n10'},
        {'n09'},
        {'n01'},
    ]

    assert sccs == expected_sccs


@stretch1
def test_edge_types():
    trees = prepost(graph1)
    edge_types = classify_edges(graph1, trees)
    expected_edge_types = {
        'tree/forward': {
            ('a', 'e'), ('a', 'f'),
            ('d', 'h'), ('d', 'i'), ('e', 'd'),
            ('f', 'b'), ('f', 'c'), ('h', 'i'),
            ('i', 'l'), ('j', 'k'), ('l', 'g')
        },
        'back': {
            ('b', 'a'), ('g', 'd'),
            ('k', 'j')
        },
        'cross': {
            ('c', 'd'), ('c', 'e'), ('j', 'f'),
            ('j', 'h'), ('k', 'i')
        }
    }

    assert edge_types == expected_edge_types


@stretch1
def test_edge_types2():
    trees = prepost(graph2)
    edge_types = classify_edges(graph2, trees)
    expected_edge_types = {
        'tree/forward': {
            ('n01', 'n02'), ('n02', 'n05'), ('n04', 'n03'), ('n05', 'n04'),
            ('n05', 'n06'), ('n06', 'n07'), ('n06', 'n08'), ('n07', 'n08')
        },
        'back': {
            ('n03', 'n02'), ('n04', 'n05'), ('n06', 'n05'),
            ('n07', 'n05'), ('n07', 'n06'), ('n08', 'n05'),
            ('n08', 'n06')
        },
        'cross': {
            ('n09', 'n07'), ('n10', 'n08')
        }
    }

    assert edge_types == expected_edge_types
