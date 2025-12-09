#include <iostream>
#include <vector>
#include "treap.cpp"

int main() {
    std::srand(time(0));
    std::cout << "Creating Treap..." << std::endl;
    Treap<int> t;
    
    // Insert 10, 20, 30, 40, 50
    for (int i = 1; i <= 5; ++i) {
        t.insert(i * 10);
    }

    std::cout << "Tree content: ";
    t.print(); // Should print 10 20 30 40 50

    std::cout << "Splitting by index 2 (first 2 elements go to left)..." << std::endl;
    Treap<int> left, right;
    t.split_by_index(2, left, right);

    std::cout << "Left tree content: ";
    left.print(); // Should print 10 20

    std::cout << "Right tree content: ";
    right.print(); // Should print 30 40 50

    std::cout << "Merging back..." << std::endl;
    left.merge(right);
    std::cout << "Merged tree content: ";
    left.print(); // Should print 10 20 30 40 50

    std::cout << "Done." << std::endl;
    return 0;
}