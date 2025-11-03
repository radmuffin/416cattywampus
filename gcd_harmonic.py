#!/usr/bin/env python3
"""
Solution for GCD-Harmonic Tree Problem

Problem: Given a tree with node values, find the minimum cost to make every pair
of adjacent nodes GCD-harmonic (i.e., gcd(a[u], a[v]) > 1).

Cost model: The cost to change a node value from x to y is |x - y|.
"""

import sys
from math import gcd
from collections import defaultdict

def read_input():
    """Read the tree input from stdin."""
    n = int(input())
    values = []
    for _ in range(n):
        values.append(int(input()))
    
    # Build adjacency list
    adj = defaultdict(list)
    for _ in range(n - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    return n, values, adj

def get_prime_factors(n):
    """Get all prime factors of n up to a reasonable limit."""
    factors = set()
    # Check small primes
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
        if n % p == 0:
            factors.add(p)
    # Check other factors
    i = 2
    while i * i <= n:
        if n % i == 0:
            factors.add(i)
            if i != n // i:
                factors.add(n // i)
        i += 1
    if n > 1:
        factors.add(n)
    return factors

def get_candidates(value, max_cost=1000):
    """
    Get candidate values near 'value' that could be used.
    We'll consider values within max_cost distance.
    """
    candidates = set()
    for delta in range(-max_cost, max_cost + 1):
        new_val = value + delta
        if new_val >= 2:  # values must be at least 2 to have gcd > 1
            candidates.add(new_val)
    return candidates

def solve_tree_dp(n, values, adj):
    """
    Solve using tree DP.
    For each node and each possible value it could take, compute minimum cost.
    """
    # Convert to 0-indexed
    values = [0] + values  # 1-indexed
    
    # Pick arbitrary root (node 1)
    root = 1
    
    # Get candidate values for each node
    candidate_range = 50  # Consider values within this range
    candidates = {}
    for i in range(1, n + 1):
        cands = set()
        for delta in range(-candidate_range, candidate_range + 1):
            new_val = values[i] + delta
            if new_val >= 2:
                cands.add(new_val)
        candidates[i] = sorted(cands)
    
    # Tree DP
    # dp[node][value] = minimum cost for subtree rooted at node if node takes 'value'
    dp = {}
    parent = {}
    
    def dfs(u, p):
        parent[u] = p
        dp[u] = {}
        
        # Get children
        children = [v for v in adj[u] if v != p]
        
        if not children:
            # Leaf node
            for val in candidates[u]:
                dp[u][val] = abs(values[u] - val)
        else:
            # Recurse on children first
            for v in children:
                dfs(v, u)
            
            # For each candidate value for u
            for u_val in candidates[u]:
                min_cost = abs(values[u] - u_val)
                
                # For each child, pick the best compatible value
                for v in children:
                    best_child_cost = float('inf')
                    for v_val in dp[v]:
                        # Check if u_val and v_val are compatible (gcd > 1)
                        if gcd(u_val, v_val) > 1:
                            best_child_cost = min(best_child_cost, dp[v][v_val])
                    
                    if best_child_cost == float('inf'):
                        # No compatible value found
                        min_cost = float('inf')
                        break
                    min_cost += best_child_cost
                
                dp[u][u_val] = min_cost
    
    dfs(root, -1)
    
    # Find minimum cost across all possible values for root
    result = min(dp[root].values()) if dp[root] else float('inf')
    return result if result != float('inf') else -1

def main():
    n, values, adj = read_input()
    
    if n == 1:
        # Single node - already GCD-harmonic (no edges)
        print(0)
        return
    
    result = solve_tree_dp(n, values, adj)
    print(result)

if __name__ == "__main__":
    main()
