#!/usr/bin/env python3
"""
Generator for GCD-Harmonic Tree test inputs.

Usage:
    python3 gen_tree_test.py <n> <max_value> <output_file>

Example:
    python3 gen_tree_test.py 1000 1000000 test_1000.txt
"""

import random
import sys
import heapq

def random_tree(n):
    """
    Generate a random tree with n nodes using Prüfer sequence.
    Returns a list of edges (u, v).
    """
    if n == 1:
        return []
    
    # Generate random Prüfer sequence
    prufer = [random.randint(1, n) for _ in range(n - 2)]
    
    # Construct tree from Prüfer sequence
    degree = [1] * (n + 1)
    for x in prufer:
        degree[x] += 1
    
    # Initialize heap with all leaves
    leaves = [i for i in range(1, n + 1) if degree[i] == 1]
    heapq.heapify(leaves)
    
    edges = []
    for p in prufer:
        leaf = heapq.heappop(leaves)
        edges.append((leaf, p))
        degree[leaf] -= 1
        degree[p] -= 1
        if degree[p] == 1:
            heapq.heappush(leaves, p)
    
    # Connect the last two nodes
    a = heapq.heappop(leaves)
    b = heapq.heappop(leaves)
    edges.append((a, b))
    
    return edges

def generate_prime_values(n, max_val):
    """
    Generate node values that are mostly prime or coprime to make the problem harder.
    """
    # List of primes up to 100
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    
    values = []
    for _ in range(n):
        if random.random() < 0.5:
            # Use a prime number
            values.append(random.choice(small_primes))
        else:
            # Use a random value
            values.append(random.randint(1, min(max_val, 100)))
    
    return values

def generate_random_values(n, max_val):
    """Generate completely random node values."""
    return [random.randint(1, max_val) for _ in range(n)]

def gen_test_file(n, max_val, filename, use_primes=False):
    """
    Generate a test input file with n nodes and maximum value max_val.
    
    Args:
        n: Number of nodes in the tree
        max_val: Maximum value for node values
        filename: Output filename
        use_primes: If True, generate mostly prime values (harder problem)
    """
    if use_primes:
        values = generate_prime_values(n, max_val)
    else:
        values = generate_random_values(n, max_val)
    
    edges = random_tree(n)
    
    with open(filename, 'w') as f:
        f.write(str(n) + '\n')
        for v in values:
            f.write(str(v) + '\n')
        for u, v in edges:
            f.write(f"{u} {v}\n")
    
    print(f"Generated {filename} with {n} nodes")

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 gen_tree_test.py <n> <max_value> <output_file> [--primes]")
        print("Example: python3 gen_tree_test.py 1000 1000000 test_1000.txt")
        sys.exit(1)
    
    n = int(sys.argv[1])
    max_val = int(sys.argv[2])
    output_file = sys.argv[3]
    use_primes = '--primes' in sys.argv
    
    gen_test_file(n, max_val, output_file, use_primes)

if __name__ == "__main__":
    main()
