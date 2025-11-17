import sys
from birthday import BS


def run_case(name, graph, expected_bridges):
    bs = BS(graph)
    found = set(bs.bs())
    expected = set(expected_bridges)
    ok = found == expected
    print(f"{name}: {'PASS' if ok else 'FAIL'}")
    if not ok:
        print("  expected:", expected)
        print("  found:   ", found)
    return ok


def main():
    tests = []

    # chain 0-1-2-3
    g1 = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
    tests.append(("chain", g1, [(0, 1), (1, 2), (2, 3)]))

    # cycle 0-1-2-0
    g2 = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
    tests.append(("cycle", g2, []))

    # disconnected: component 0-1 and isolated 2
    g3 = {0: [1], 1: [0], 2: []}
    tests.append(("disconnected", g3, [(0, 1)]))

    # single edge with inferred n from neighbors
    g4 = {2: [3], 3: [2]}
    tests.append(("inferred_n", g4, [(2, 3)]))

    all_ok = True
    for name, graph, expected in tests:
        ok = run_case(name, graph, expected)
        all_ok = all_ok and ok

    if all_ok:
        print("ALL TESTS PASSED")
        return 0
    else:
        print("SOME TESTS FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(main())

