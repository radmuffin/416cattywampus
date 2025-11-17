#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
using namespace std;

struct Event {
    int x, type, y1, y2;
    Event(int x, int type, int y1, int y2) : x(x), type(type), y1(y1), y2(y2) {}
    bool operator<(const Event& other) const {
        if (x != other.x) return x < other.x;
        return type > other.type; // Process end events (-1) before start events (1) for the same x
    }
};

bool rectangles_intersect_sweep(const vector<vector<int>>& rectangles) {
    vector<Event> events;
    for (const auto& rect : rectangles) {
        int x1 = rect[0], y1 = rect[1], x2 = rect[2], y2 = rect[3];
        events.emplace_back(x1, 1, y1, y2);  // Start of a rectangle
        events.emplace_back(x2, -1, y1, y2); // End of a rectangle
    }

    // Sort events by x-coordinate, then by type
    sort(events.begin(), events.end());

    // Active intervals in the y-dimension
    set<pair<int, int>> active_intervals;

    for (const auto& event : events) {
        int y1 = event.y1, y2 = event.y2;
        if (event.type == 1) { // Start of a rectangle
            // Check for intersections with active intervals
            auto it = active_intervals.lower_bound({y1, -1});
            if (it != active_intervals.end() && it->first < y2) {
                return true; // Overlap found
            }
            for (auto it2 = active_intervals.begin(); it2 != it; ++it2) {
                if (it2->second > y1) {
                    return true; // Overlap found
                }
            }
            // Add current rectangle's y-interval to active intervals
            active_intervals.insert({y1, y2});
        } else if (event.type == -1) { // End of a rectangle
            // Remove the rectangle's y-interval from active intervals
            active_intervals.erase({y1, y2});
        }
    }

    return false; // No intersections found
}

int main() {
    int n;
    cin >> n;
    vector<vector<int>> rectangles(n, vector<int>(4));
    for (int i = 0; i < n; ++i) {
        cin >> rectangles[i][0] >> rectangles[i][1] >> rectangles[i][2] >> rectangles[i][3];
    }
    cout << (rectangles_intersect_sweep(rectangles) ? "1" : "0") << endl;
    return 0;
}