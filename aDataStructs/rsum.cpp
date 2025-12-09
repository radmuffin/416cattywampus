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
        long long sum;
        bool rev;
        Node* left;
        Node* right;
        
        Node(T val) : value(val), priority(std::rand() % MX), sum(val), size(1), rev(false), left(nullptr), right(nullptr) {}
    };

private:
    Node* root;

    int cnt(Node* n) {
        return n ? n->size : 0;
    }

    long long addd(Node* n) {
        return n ? n->sum : 0;
    }

    void upd(Node* n) {
        if (n) {
            n->size = 1 + cnt(n->left) + cnt(n->right);
            n->sum = n->value + addd(n->left) + addd(n->right);
        }
    }

    void push(Node* n) {
        if (n && n->rev) {
            n->rev = false;
            std::swap(n->left, n->right);
            if (n->left) n->left->rev ^= true;
            if (n->right) n->right->rev ^= true;
        }
    }
    
    // Split by size: left gets k nodes, right gets the rest
    void split_by_size(Node* node, int k, Node*& left, Node*& right) {
        if (!node) {
            left = right = nullptr;
            return;
        }
        push(node);
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
        push(left);
        push(right);
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

    int print(Node* node) {
        if (!node) return 0;
        int sum = node->value;
        // push(node);
        sum += print(node->left);
        // std::cout << node->value;
        sum += print(node->right);
        return sum;
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

    bool empty() const {
        return root == nullptr;
    }

    void print() {
        std::cout << print(root);
        std::cout << "\n";
    }

    void split_by_index(int k, Treap<T>& leftTreap, Treap<T>& rightTreap) {
        split_by_size(root, k, leftTreap.root, rightTreap.root);
        root = nullptr;
    }
    
    void merge(Treap<T>& other) {
        merge(root, root, other.root);
        other.root = nullptr;
    }

    long long getSum() {
        return root->sum;
    }

    void flip() {
        if (root) root->rev ^= true;
    }
};

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);
    int n,m;
    std::cin >> n >> m;
    Treap<long> t = Treap<long>();
    for (int i = 0; i < n; i++) {
        long c;
        std::cin >> c;
        t.append(c);
    }
    for (int i = 0; i < m; i++) {
        int o,l,r;
        std::cin >> o >> l >> r;
        Treap<long> left, temp, middle, right;
        t.split_by_index(l-1, left, temp);
        temp.split_by_index(r-l+1, middle, right);
        if (o == 1) { //reverse
            middle.flip();
        }
        else { //sum and print
            std::cout << middle.getSum() << '\n';
        }
        t.merge(left);
        t.merge(middle);
        t.merge(right);
    }
}