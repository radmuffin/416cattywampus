#!/usr/bin/env python3
"""
Test script to verify pruning effectiveness in flowfree.py
"""

import subprocess
import time
import sys

def test_case(name, input_data, expected_output):
    """Run a test case and measure time."""
    print(f"\nTesting {name}...")
    start = time.time()
    
    try:
        result = subprocess.run(
            ['python3', 'flowfree.py'],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=10
        )
        elapsed = time.time() - start
        
        output = result.stdout.strip()
        success = output == expected_output
        
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} - {elapsed:.3f}s")
        print(f"  Expected: {expected_output}")
        print(f"  Got: {output}")
        
        return success
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        print(f"✗ TIMEOUT after {elapsed:.1f}s")
        return False

def main():
    all_pass = True
    
    # Test 1: Simple solvable (sol.txt)
    with open('sol.txt', 'r') as f:
        sol_input = f.read()
    all_pass &= test_case("sol.txt", sol_input, "solvable")
    
    # Test 2: Not solvable (nsol.txt)
    with open('nsol.txt', 'r') as f:
        nsol_input = f.read()
    all_pass &= test_case("nsol.txt", nsol_input, "not solvable")
    
    # Test 3: Larger solvable puzzle (same row, Hamiltonian path exists)
    test3 = """4
a..a
....
....
....
"""
    all_pass &= test_case("4x4 solvable (simple)", test3, "solvable")
    
    # Test 4: Impossible due to parity
    test4 = """4
a...
....
....
...a
"""
    all_pass &= test_case("4x4 impossible (isolated)", test4, "not solvable")
    
    # Test 5: 5x5 solvable (single color)
    test5 = """5
a....
.....
.....
.....
....a
"""
    all_pass &= test_case("5x5 solvable (simple)", test5, "solvable")
    
    print("\n" + "="*50)
    if all_pass:
        print("All tests PASSED!")
        return 0
    else:
        print("Some tests FAILED!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
