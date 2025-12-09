#include <iostream>
#include <vector>
#include "treap.cpp"

int main() {
    std::srand(time(0));
    std::cout << "Creating Treap..." << std::endl;
    Treap<int> t;
    
    std::cout << "Inserting 5, 3, 7, 5..." << std::endl;
    t.insert(5);
    t.insert(3);
    t.insert(7);
    t.insert(5);

    std::cout << "Tree content: ";
    t.print(); // Should print 3 5 5 7 (inorder)

    std::cout << "Erasing 5..." << std::endl;
    t.erase(5);
    
    std::cout << "Tree content after erase: ";
    t.print(); // Should print 3 5 7

    std::cout << "Erasing 5 again..." << std::endl;
    t.erase(5);
    
    std::cout << "Tree content after second erase: ";
    t.print(); // Should print 3 7

    std::cout << "Erasing 7..." << std::endl;
    t.erase(7);
    std::cout << "Tree content after erasing 7: ";
    t.print(); // Should print 3

    std::cout << "Erasing 3..." << std::endl;
    t.erase(3);
    std::cout << "Tree content after erasing 3: ";
    t.print(); // Should be empty

    std::cout << "Done." << std::endl;
    return 0;
}
