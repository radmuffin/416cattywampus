# GCD-Harmonic Tree Problem

## Problem Statement

Given a tree with undirected edges where each node has an integer value, find the minimum total cost to make every pair of adjacent nodes GCD-harmonic (i.e., their GCD > 1).

**Cost Model:** You can change any node's value to any positive integer. The cost of changing a node to value `v` is `v`. Keeping the original value costs 0.

## Files

- **gcd_harmonic.py** - Solution implementation (tree DP)
- **gen_tree_test.py** - Test input generator
- **gcd1.txt** - Test input (expected output: 6)
- **gcd2.txt** - Test input (expected output: 4)
- **TEST_RESULTS.md** - Comprehensive test results and performance analysis

## Usage

### Running the Solution

```bash
python3 gcd_harmonic.py < gcd1.txt
# Output: 6

python3 gcd_harmonic.py < gcd2.txt
# Output: 4
```

### Generating Test Inputs

Generate a random tree with `n` nodes and values up to `max_val`:
```bash
python3 gen_tree_test.py <n> <max_val> <output_file>

# Examples:
python3 gen_tree_test.py 100 1000 test_100.txt
python3 gen_tree_test.py 1000 10000 test_1000.txt
```

Generate with mostly prime values (harder test case):
```bash
python3 gen_tree_test.py 100 1000 test_100_primes.txt --primes
```

## Input Format

```
n                    # number of nodes
a_1                  # value of node 1
a_2                  # value of node 2
...
a_n                  # value of node n
u_1 v_1              # edge 1
u_2 v_2              # edge 2
...
u_(n-1) v_(n-1)      # edge n-1
```

## Example: gcd1.txt

```
3
7
11
13
1 2
1 3
```

**Tree structure:** Node 1 is connected to nodes 2 and 3 (star topology)
**Node values:** [7, 11, 13] (all prime)

**Optimal solution:**
- Change node 1 to 2 (cost: 2)
- Change node 2 to 2 (cost: 2)  
- Change node 3 to 2 (cost: 2)
- Total cost: 6
- Result: All adjacent pairs have gcd(2,2) = 2 > 1 ✓

## Example: gcd2.txt

```
2
7
11
1 2
```

**Tree structure:** Simple edge between nodes 1 and 2
**Node values:** [7, 11] (both prime)

**Optimal solution:**
- Change node 1 to 2 (cost: 2)
- Change node 2 to 2 (cost: 2)
- Total cost: 4
- Result: gcd(2,2) = 2 > 1 ✓

## Algorithm

The solution uses dynamic programming on trees:

1. **State:** `dp[node][value]` = minimum cost for subtree rooted at `node` if `node` has `value`
2. **Candidates:** For each node, consider:
   - Keeping original value (cost 0)
   - Changing to small values 2-50 (small cost, good divisibility)
3. **Transition:** For each node, try each candidate value and pick the minimum cost compatible assignment for all children
4. **Constraint:** Adjacent nodes must have gcd > 1

**Time Complexity:** O(n × C²) where C is the number of candidates (~50-100)
**Space Complexity:** O(n × C)

## Performance

See TEST_RESULTS.md for detailed performance analysis. Summary:
- n=100: ~3 seconds
- n=1000 (primes): ~1 second
- n=5000 (primes): ~6 seconds
