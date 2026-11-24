#include <iostream>
#include <string>
using namespace std;

// node of the Huffman tree
struct Node {
    char ch;
    int freq;
    int order;   // creation order, used to break ties between equal frequencies
    Node* left;
    Node* right;
    Node(char c, int f, int o) {
        ch = c;
        freq = f;
        order = o;
        left = nullptr;
        right = nullptr;
    }
};

// array based binary min heap of Node pointers
struct MinHeap {
    Node* a[100];
    int size;
    MinHeap() {
        size = 0;
    }
    bool smaller(Node* x, Node* y) {
        if (x->freq != y->freq)
            return x->freq < y->freq;
        return x->order < y->order;
    }
    void swapAt(int i, int j) {
        Node* t = a[i];
        a[i] = a[j];
        a[j] = t;
    }
    void push(Node* n) {
        a[size] = n;
        int i = size++;
        // sift up
        while (i > 0 && smaller(a[i], a[(i - 1) / 2])) {
            swapAt(i, (i - 1) / 2);
            i = (i - 1) / 2;
        }
    }
    Node* pop() {
        Node* top = a[0];
        a[0] = a[--size];
        int i = 0;
        // sift down
        while (true) {
            int l = 2 * i + 1, r = 2 * i + 2, m = i;
            if (l < size && smaller(a[l], a[m]))
                m = l;
            if (r < size && smaller(a[r], a[m]))
                m = r;
            if (m == i)
                break;
            swapAt(i, m);
            i = m;
        }
        return top;
    }
};

Node* buildHuffman(string s, int f[], int n) {
    MinHeap h;
    int order = 0;
    for (int i = 0; i < n; i++)
        h.push(new Node(s[i], f[i], order++));
    while (h.size > 1) {
        Node* x = h.pop();   // smallest goes left
        Node* y = h.pop();
        Node* z = new Node('$', x->freq + y->freq, order++);
        z->left = x;
        z->right = y;
        h.push(z);
    }
    return h.pop();
}

// preorder: root, left (add 0), right (add 1); codes are printed at the leaves
void preorder(Node* root, string code) {
    if (root == nullptr)
        return;
    if (root->left == nullptr && root->right == nullptr) {
        cout << "  " << root->ch << " (" << root->freq << ") : "
             << (code == "" ? "0" : code) << endl;
        return;
    }
    preorder(root->left, code + "0");
    preorder(root->right, code + "1");
}

void freeTree(Node* root) {
    if (root == nullptr)
        return;
    freeTree(root->left);
    freeTree(root->right);
    delete root;
}

void solve(string s, int f[], int n) {
    cout << "S = " << s << ", f = {";
    for (int i = 0; i < n; i++)
        cout << f[i] << (i < n - 1 ? ", " : "}");
    cout << endl;
    Node* root = buildHuffman(s, f, n);
    cout << "Huffman codes in preorder:" << endl;
    preorder(root, "");
    freeTree(root);
    cout << endl;
}

int main() {
    int f1[] = {5, 9, 12, 13, 16, 45};
    solve("abcdef", f1, 6);

    int f2[] = {10, 15, 12, 3, 4, 13, 1};
    solve("aeioust", f2, 7);

    int f3[] = {7};
    solve("z", f3, 1);
    return 0;
}
