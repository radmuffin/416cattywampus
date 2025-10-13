# this is absolutely an ai solution. However I understand the implementation. I need better time management.
# too slowwwwwww
# need to only compare to certain values in seg tree
# point compression???


class SegmentTree:
    def __init__(self, min_y, max_y):
        self.min_y = min_y
        self.max_y = max_y
        self.tree = [0] * (4 * (max_y - min_y + 1))

    def _update(self, node, start, end, l, r, value):
        if r < start or l > end:  # No overlap
            return
        if l <= start and end <= r:  # Full overlap
            self.tree[node] += value
            return
        # Partial overlap
        mid = (start + end) // 2
        self._update(2 * node + 1, start, mid, l, r, value)
        self._update(2 * node + 2, mid + 1, end, l, r, value)

    def update(self, l, r, value):
        self._update(0, self.min_y, self.max_y, l, r, value)

    def _query(self, node, start, end, l, r):
        if r < start or l > end:  # No overlap
            return 0
        if l <= start and end <= r:  # Full overlap
            return self.tree[node]
        # Partial overlap
        mid = (start + end) // 2
        left = self._query(2 * node + 1, start, mid, l, r)
        right = self._query(2 * node + 2, mid + 1, end, l, r)
        return left + right

    def query(self, l, r):
        return self._query(0, self.min_y, self.max_y, l, r)


def rectangles_intersect_sweep(rectangles):
    events = []  # Store events for the sweep line
    y_coords = set()
    for x1, y1, x2, y2 in rectangles:
        events.append((x1, 1, y1, y2))  # Rectangle start event
        events.append((x2, -1, y1, y2))  # Rectangle end event
        y_coords.add(y1)
        y_coords.add(y2)

    # Coordinate compression for y-coordinates
    y_map = {y: i for i, y in enumerate(sorted(y_coords))}
    max_y = len(y_map) - 1

    # Sort events by x-coordinate, then by type (-1 before 1 for same x)
    events.sort()

    # Segment tree for active intervals
    seg_tree = SegmentTree(0, max_y)

    for x, event_type, y1, y2 in events:
        y1, y2 = y_map[y1], y_map[y2] - 1  # Map y-coordinates to compressed indices
        if event_type == 1:  # Start of a rectangle
            # Check for intersections with active intervals
            if seg_tree.query(y1, y2) > 0:
                return 1
            # Add current rectangle's y-interval to active intervals
            seg_tree.update(y1, y2, 1)
        elif event_type == -1:  # End of a rectangle
            # Remove the rectangle's y-interval from active intervals
            seg_tree.update(y1, y2, -1)

    return 0  # No intersections found


# Input handling
import sys
input = sys.stdin.read
data = input().splitlines()
n = int(data[0])
rectangles = [tuple(map(int, line.split())) for line in data[1:]]
print(rectangles_intersect_sweep(rectangles))