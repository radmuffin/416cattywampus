#!/usr/bin/env python3
"""
Flow Free Puzzle Solver with Pruning
Solves Flow Free puzzles using backtracking with pruning optimizations.
"""

def parse_input():
    """Parse input and return grid size and color endpoints."""
    size = int(input())
    grid = []
    for _ in range(size):
        grid.append(list(input().strip()))
    
    # Find all color endpoints
    colors = {}
    for i in range(size):
        for j in range(size):
            if grid[i][j] != '.':
                color = grid[i][j]
                if color not in colors:
                    colors[color] = []
                colors[color].append((i, j))
    
    return size, grid, colors


def pruneWorthy(grid, size, colors, filled_count):
    """
    Check if current state is worth pruning (should abandon this branch).
    Returns True if we should prune (abandon), False if we should continue.
    
    Pruning conditions:
    1. Check for isolated empty cells (cells that can't be reached)
    2. Check if any color pair is blocked from connecting
    3. Check for cells with no valid neighbors
    """
    # Check for isolated cells or unreachable regions
    for i in range(size):
        for j in range(size):
            if grid[i][j] == '.':
                # Check if this empty cell has at least one valid neighbor
                neighbors = get_neighbors(i, j, size)
                has_valid_neighbor = False
                for ni, nj in neighbors:
                    if grid[ni][nj] == '.' or grid[ni][nj].islower():
                        has_valid_neighbor = True
                        break
                
                if not has_valid_neighbor:
                    # This cell is surrounded by completed paths, can't be filled
                    return True
    
    # Check if any unconnected color pair is blocked
    for color, endpoints in colors.items():
        if len(endpoints) != 2:
            continue
        
        start, end = endpoints
        if grid[start[0]][start[1]] == color.upper():
            # This color is already connected, skip
            continue
        
        # Check if path still possible using simple BFS reachability
        if not is_reachable(grid, size, start, end, color):
            return True
    
    return False


def is_reachable(grid, size, start, end, color):
    """
    Quick BFS check to see if end is reachable from start.
    Only checks if path is possible, not if it fills the grid.
    """
    if start == end:
        return True
    
    visited = set()
    queue = [start]
    visited.add(start)
    
    while queue:
        i, j = queue.pop(0)
        
        for ni, nj in get_neighbors(i, j, size):
            if (ni, nj) in visited:
                continue
            
            cell = grid[ni][nj]
            # Can move to empty cells or cells with our color (including endpoint)
            if cell == '.' or cell == color or cell == color.lower():
                if (ni, nj) == end:
                    return True
                visited.add((ni, nj))
                queue.append((ni, nj))
    
    return False


def get_neighbors(i, j, size):
    """Get valid neighboring cells (up, down, left, right)."""
    neighbors = []
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < size and 0 <= nj < size:
            neighbors.append((ni, nj))
    return neighbors


def solve(grid, size, colors, current_color_idx, color_list, filled_count):
    """
    Backtracking solver with pruning.
    Returns True if puzzle is solvable, False otherwise.
    """
    total_cells = size * size
    
    # Base case: all cells filled
    if filled_count == total_cells:
        return True
    
    # Pruning: check if we should abandon this branch
    if pruneWorthy(grid, size, colors, filled_count):
        return False
    
    # If we've tried all colors, fail
    if current_color_idx >= len(color_list):
        return False
    
    color = color_list[current_color_idx]
    endpoints = colors[color]
    
    if len(endpoints) != 2:
        # Invalid puzzle
        return False
    
    start, end = endpoints
    
    # Try to connect this color
    if connect_color(grid, size, start, end, color, colors, color_list, filled_count):
        return True
    
    # Try next color
    return solve(grid, size, colors, current_color_idx + 1, color_list, filled_count)


def connect_color(grid, size, start, end, color, colors, color_list, filled_count):
    """
    Try to connect a color pair using DFS.
    Returns True if connection leads to solution, False otherwise.
    """
    si, sj = start
    ei, ej = end
    
    # DFS to find path from start to end
    def dfs(i, j, path):
        if (i, j) == end:
            # Found the endpoint, mark the path
            for pi, pj in path[1:-1]:  # Exclude endpoints
                grid[pi][pj] = color.lower()
            
            # Mark this color as connected
            grid[si][sj] = color.upper()
            grid[ei][ej] = color.upper()
            
            new_filled = filled_count + len(path)
            
            # Try to solve rest of puzzle
            next_idx = color_list.index(color) + 1
            
            if solve(grid, size, colors, next_idx, color_list, new_filled):
                return True
            
            # Backtrack
            for pi, pj in path[1:-1]:
                grid[pi][pj] = '.'
            grid[si][sj] = color
            grid[ei][ej] = color
            
            return False
        
        # Try each neighbor
        for ni, nj in get_neighbors(i, j, size):
            if (ni, nj) in path:
                continue
            
            cell = grid[ni][nj]
            
            # Can move to empty cells or the endpoint
            if cell == '.' or (ni, nj) == end:
                path.append((ni, nj))
                if dfs(ni, nj, path):
                    return True
                path.pop()
        
        return False
    
    return dfs(si, sj, [start])


def main():
    size, grid, colors = parse_input()
    
    # Count initially filled cells (the color endpoints)
    filled_count = sum(1 for i in range(size) for j in range(size) if grid[i][j] != '.')
    
    color_list = list(colors.keys())
    
    if solve(grid, size, colors, 0, color_list, filled_count):
        print("solvable")
    else:
        print("not solvable")


if __name__ == "__main__":
    main()
