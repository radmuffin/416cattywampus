# GCD-Harmonic Tree - Test Results

## Problem Description
Given a tree with node values, find the minimum cost to make every pair of adjacent nodes GCD-harmonic (i.e., gcd(a[u], a[v]) > 1).

**Cost Model:** The cost to change a node to value v is v (the new value itself). Keeping the original value costs 0.

## Solution Approach
Dynamic Programming on trees:
- For each node, consider keeping its original value (cost 0) or changing it to a candidate value (cost = new value)
- Use tree DP to compute minimum cost for each subtree
- Candidate values include: original values + small values (2-50)

## Test Results

### Small Test Cases (Verification)
| Test File | Nodes | Expected Output | Actual Output | Status |
|-----------|-------|----------------|---------------|--------|
| gcd1.txt  | 3     | 6              | 6             | ✓ PASS |
| gcd2.txt  | 2     | 4              | 4             | ✓ PASS |

#### gcd1.txt
```
3 nodes: values [7, 11, 13] in a star topology
Edges: 1-2, 1-3
Optimal solution: Change nodes 2 and 3 to value 2 each (cost 2+2=4)
                  Change node 1 to value 2 (cost 2)
                  Total cost: 6
```

#### gcd2.txt
```
2 nodes: values [7, 11] 
Edge: 1-2
Optimal solution: Change both nodes to value 2 (cost 2+2=4)
```

### Performance Testing

| Test Case | Nodes (n) | Max Value | Type | Output | Time (seconds) |
|-----------|-----------|-----------|------|--------|----------------|
| test_100.txt | 100 | 1000 | Random | 87 | 2.77 |
| test_100_primes.txt | 100 | 1000 | Primes | 142 | 0.36 |
| test_500.txt | 500 | 10000 | Random | 550 | 17.52 |
| test_1000.txt | 1000 | 10000 | Random | 901 | 133.92 |
| test_1000_primes.txt | 1000 | 10000 | Primes | 1467 | 1.16 |
| test_5000_primes.txt | 5000 | 10000 | Primes | 7231 | 5.75 |

### Observations

1. **Small values dominate:** The optimal solutions tend to use small values (2-50) because:
   - Cost = value itself, so smaller is better
   - Small values like 2, 3, 4, 6 have many common factors
   
2. **Prime inputs are easier:** When inputs are mostly prime numbers, the solution is faster because:
   - The optimal choice is clear: change everything to small composites like 2, 4, 6
   - Less branching in the DP

3. **Random inputs are harder:** When inputs have large random values:
   - More candidates to consider (all original values)
   - Original values might be large, making it expensive to keep them
   - Solution takes longer to compute

4. **Scalability:** The solution handles:
   - n=100 in < 3 seconds
   - n=1000 in ~2 minutes (random) or ~1 second (primes)
   - n=5000 in ~6 seconds (primes)

## Files
- `gcd_harmonic.py` - Solution implementation
- `gen_tree_test.py` - Test input generator
- `gcd1.txt`, `gcd2.txt` - Small test cases
- `test_*.txt` - Generated larger test cases
