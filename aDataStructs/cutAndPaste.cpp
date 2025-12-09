#include <cstdlib>
#include <ctime>
#include <iostream>

const int MX = 1 << 30; // Maximum priority value (2^30, safe for int range)

template <typename T>
class Treap {
public:
    struct Node {
        T value;
        int priority;
        int size;
        Node* left;
        Node* right;
        
        Node(T val) : value(val), priority(std::rand() % MX), size(1), left(nullptr), right(nullptr) {}
    };

private:
    Node* root;

    int cnt(Node* n) {
        return n ? n->size : 0;
    }

    void upd(Node* n) {
        if (n) {
            n->size = 1 + cnt(n->left) + cnt(n->right);
        }
    }
    
    // Split into <= key and > key
    void split(Node* node, T key, Node*& left, Node*& right) {
        if (!node) {
            left = right = nullptr;
        } else if (node->value <= key) {
            split(node->right, key, node->right, right);
            left = node;
        } else {
            split(node->left, key, left, node->left);
            right = node;
        }
        upd(node);
    }

    // Split into < key and >= key
    void split_less(Node* node, T key, Node*& left, Node*& right) {
        if (!node) {
            left = right = nullptr;
        } else if (node->value < key) {
            split_less(node->right, key, node->right, right);
            left = node;
        } else {
            split_less(node->left, key, left, node->left);
            right = node;
        }
        upd(node);
    }

    // Split by size: left gets k nodes, right gets the rest
    void split_by_size(Node* node, int k, Node*& left, Node*& right) {
        if (!node) {
            left = right = nullptr;
            return;
        }
        int l_cnt = cnt(node->left);
        if (l_cnt >= k) {
            split_by_size(node->left, k, left, node->left);
            right = node;
        } else {
            split_by_size(node->right, k - l_cnt - 1, node->right, right);
            left = node;
        }
        upd(node);
    }

    void merge(Node*& node, Node* left, Node* right) {
        if (!left || !right) {
            node = left ? left : right;
        } else if (left->priority > right->priority) {
            merge(left->right, left->right, right);
            node = left;
        } else {
            merge(right->left, left, right->left);
            node = right;
        }
        upd(node);
    }

    void clear(Node* node) {
        if (!node) return;
        clear(node->left);
        clear(node->right);
        delete node;
    }

    void print(Node* node) {
        if (!node) return;
        print(node->left);
        std::cout << node->value;
        print(node->right);
    }

public:
    Treap() : root(nullptr) {}
    ~Treap() { clear(root); }
    
    void insert(T value) {
        Node* newNode = new Node(value);
        Node *left = nullptr, *right = nullptr;
        split(root, value, left, right);
        merge(left, left, newNode);
        merge(root, left, right);
    }

    void append(T value) {
        Node* newNode = new Node(value);
        merge(root, root, newNode);
    }

    void erase(T value) {
        Node *less = nullptr, *equal = nullptr, *greater = nullptr;
        split_less(root, value, less, equal); // less: < value, equal: >= value
        split(equal, value, equal, greater);  // equal: == value, greater: > value
        
        if (equal) {
            // Remove one instance (the root of the 'equal' treap)
            Node* temp = equal;
            merge(equal, equal->left, equal->right);
            delete temp;
        }
        
        merge(root, less, equal);
        merge(root, root, greater);
    }

    bool find(T value) {
        Node* curr = root;
        while (curr) {
            if (curr->value == value) return true;
            if (curr->value < value) curr = curr->right;
            else curr = curr->left;
        }
        return false;
    }

    bool empty() const {
        return root == nullptr;
    }

    void print() {
        print(root);
        std::cout << std::endl;
    }
    
    void split(T key, Treap<T>& leftTreap, Treap<T>& rightTreap) {
        split(root, key, leftTreap.root, rightTreap.root);
        root = nullptr; 
    }

    void split_by_index(int k, Treap<T>& leftTreap, Treap<T>& rightTreap) {
        split_by_size(root, k, leftTreap.root, rightTreap.root);
        root = nullptr;
    }
    
    void merge(Treap<T>& other) {
        merge(root, root, other.root);
        other.root = nullptr;
    }
};


int main() {
    std::srand(std::time(0));
    int n, m;
    std::cin >> n >> m;
    std::string s;
    std::cin >> s;
    Treap<char> t = Treap<char>();
    for (char c : s) {
        t.append(c);
    }
    for (int i = 0; i < m; i++) {
        int l, r;
        std::cin >> l >> r;
        Treap<char> left, temp, middle, right;
        t.split_by_index(l - 1, left, temp);
        temp.split_by_index(r - l + 1, middle, right);
        
        // left.print();
        // middle.print();
        // right.print();


        t.merge(left);
        t.merge(right);
        t.merge(middle);
        // std::cout << "After cut-and-paste " << (i + 1) << ": ";
        // t.print();
    }
    t.print();

    return 0;
}