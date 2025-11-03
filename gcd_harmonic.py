#!/usr/bin/env python3
"""
Solution for GCD-Harmonic Tree Problem

Problem: Given a tree with node values, find the minimum cost to make every pair
of adjacent nodes GCD-harmonic (i.e., gcd(a[u], a[v]) > 1).

Cost model: The cost to change a node to value v is v (the new value itself).
If we keep the original value, cost is 0.
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

def solve_tree_dp(n, values, adj):
    """
    Solve using tree DP.
    For each node, we can either:
    1. Keep its original value (cost 0)
    2. Change it to a new value v (cost v)
    
    We want all adjacent nodes to have gcd > 1.
    """
    # Convert to 1-indexed
    values = [0] + values  # values[1] to values[n]
    
    if n == 1:
        return 0
    
    # Pick arbitrary root (node 1)
    root = 1
    
    # Generate candidate values to try
    # We'll try: original values, and small multiples/values that might work
    candidate_set = set()
    
    # Add all original values
    for v in values[1:]:
        candidate_set.add(v)
    
    # Add small values that might be good (cheap options)
    for v in range(2, 101):  # Small values are cheap
        candidate_set.add(v)
    
    # Add factors and multiples of original values
    for v in values[1:]:
        # Add small multiples
        for mult in range(1, 4):
            if v * mult <= 10000:
                candidate_set.add(v * mult)
        # Add factors
        for d in range(2, min(v, 101)):
            if v % d == 0:
                candidate_set.add(d)
                if v // d <= 10000:
                    candidate_set.add(v // d)
    
    candidates = sorted(candidate_set)
    
    # Tree DP
    # dp[node][value] = minimum cost for subtree rooted at node if node has 'value'
    # value can be original (index -1) or one of the candidates
    dp = {}
    
    def dfs(u, p):
        dp[u] = {}
        
        # Get children
        children = [v for v in adj[u] if v != p]
        
        if not children:
            # Leaf node
            # Option 1: Keep original value
            dp[u][values[u]] = 0
            
            # Option 2: Change to a candidate value
            for cand in candidates:
                if cand != values[u]:
                    dp[u][cand] = cand
        else:
            # Recurse on children first
            for v in children:
                dfs(v, u)
            
            # Try keeping original value for u
            u_val = values[u]
            cost = 0
            possible = True
            
            for v in children:
                best_child = float('inf')
                for v_val in dp[v]:
                    if gcd(u_val, v_val) > 1:
                        best_child = min(best_child, dp[v][v_val])
                
                if best_child == float('inf'):
                    possible = False
                    break
                cost += best_child
            
            if possible:
                dp[u][u_val] = cost
            
            # Try changing u to each candidate value
            for cand in candidates:
                if cand == values[u]:
                    continue  # Already handled above
                
                cost = cand  # Cost to change u to cand
                possible = True
                
                for v in children:
                    best_child = float('inf')
                    for v_val in dp[v]:
                        if gcd(cand, v_val) > 1:
                            best_child = min(best_child, dp[v][v_val])
                    
                    if best_child == float('inf'):
                        possible = False
                        break
                    cost += best_child
                
                if possible:
                    dp[u][cand] = cost
    
    dfs(root, -1)
    
    # Find minimum cost across all possible values for root
    if not dp[root]:
        return -1
    
    result = min(dp[root].values())
    return result if result != float('inf') else -1

def main():
    n, values, adj = read_input()
    result = solve_tree_dp(n, values, adj)
    print(result)

if __name__ == "__main__":
    main()
