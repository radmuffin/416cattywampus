#include <iostream>
#include <vector>
#include "rev.cpp"

int main() {
    std::srand(time(0));
    std::cout << "Creating Treap..." << std::endl;
    Treap<int> t;
    
    // Insert 1, 2, 3, 4, 5
    for (int i = 1; i <= 5; ++i) {
        t.append(i);
    }

    std::cout << "Tree content: ";
    t.print(); // Should print 12345
    std::cout << std::endl;

    std::cout << "Flipping entire tree..." << std::endl;
    t.flip();
    
    std::cout << "Tree content after flip: ";
    t.print(); // Should print 54321
    std::cout << std::endl;

    std::cout << "Splitting first 2 elements (which are 5, 4)..." << std::endl;
    Treap<int> left, right;
    t.split_by_index(2, left, right);
    
    std::cout << "Left: "; left.print(); std::cout << std::endl; // 54
    std::cout << "Right: "; right.print(); std::cout << std::endl; // 321
    
    std::cout << "Flipping Left (54 -> 45)..." << std::endl;
    left.flip();
    
    std::cout << "Merging Left and Right..." << std::endl;
    left.merge(right);
    
    std::cout << "Final: ";
    left.print(); // Should be 45321
    std::cout << std::endl;

    return 0;
}