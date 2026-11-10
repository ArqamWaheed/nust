#include <iostream>
using namespace std;

struct Node {
    int key;
    Node* left;
    Node* right;
    Node(int k) {
        key = k;
        left = nullptr;
        right = nullptr;
    }
};

Node* insert(Node* root, int key) {
    if (root == nullptr)
        return new Node(key);
    if (key < root->key)
        root->left = insert(root->left, key);
    else if (key > root->key)
        root->right = insert(root->right, key);
    return root;
}

void inorder(Node* root) {
    if (root == nullptr)
        return;
    inorder(root->left);
    cout << root->key << " ";
    inorder(root->right);
}

// walk down from the root: going right means the node is a predecessor
// candidate, going left means it is a successor candidate
void findPreSuc(Node* root, int key, Node*& pre, Node*& suc) {
    pre = nullptr;
    suc = nullptr;
    Node* cur = root;
    while (cur != nullptr) {
        if (key < cur->key) {
            suc = cur;
            cur = cur->left;
        } else if (key > cur->key) {
            pre = cur;
            cur = cur->right;
        } else {
            // key found, pre is the max of left subtree, suc is min of right subtree
            if (cur->left != nullptr) {
                pre = cur->left;
                while (pre->right != nullptr)
                    pre = pre->right;
            }
            if (cur->right != nullptr) {
                suc = cur->right;
                while (suc->left != nullptr)
                    suc = suc->left;
            }
            return;
        }
    }
}

// recursive range query, skips subtrees that cannot have keys in [lo, hi]
void rangeRecursive(Node* root, int lo, int hi, int& comparisons) {
    if (root == nullptr)
        return;
    comparisons++;
    if (root->key > lo)
        rangeRecursive(root->left, lo, hi, comparisons);
    comparisons++;
    if (root->key >= lo && root->key <= hi)
        cout << root->key << " ";
    comparisons++;
    if (root->key < hi)
        rangeRecursive(root->right, lo, hi, comparisons);
}

// iterative range query, inorder walk with an explicit stack
void rangeIterative(Node* root, int lo, int hi, int& comparisons) {
    Node* stack[100];
    int top = -1;
    Node* cur = root;
    while (cur != nullptr || top != -1) {
        while (cur != nullptr) {
            stack[++top] = cur;
            comparisons++;
            if (cur->key > lo)
                cur = cur->left;
            else
                cur = nullptr;
        }
        cur = stack[top--];
        comparisons++;
        if (cur->key >= lo && cur->key <= hi)
            cout << cur->key << " ";
        comparisons++;
        if (cur->key < hi)
            cur = cur->right;
        else
            cur = nullptr;
    }
}

int main() {
    int values[] = {50, 30, 70, 20, 40, 60, 80, 35, 45, 65, 85};
    int n = sizeof(values) / sizeof(values[0]);
    Node* root = nullptr;
    for (int i = 0; i < n; i++)
        root = insert(root, values[i]);

    cout << "Inserted: ";
    for (int i = 0; i < n; i++)
        cout << values[i] << " ";
    cout << "\nInorder : ";
    inorder(root);
    cout << "\n";

    int key, lo, hi;
    cout << "\nEnter key for predecessor/successor: ";
    cin >> key;
    Node* pre;
    Node* suc;
    findPreSuc(root, key, pre, suc);
    cout << "Predecessor of " << key << ": ";
    if (pre) cout << pre->key; else cout << "none";
    cout << "\nSuccessor of " << key << "  : ";
    if (suc) cout << suc->key; else cout << "none";
    cout << "\n";

    cout << "\nEnter range (low high): ";
    cin >> lo >> hi;
    int recCount = 0, itCount = 0;
    cout << "Recursive range [" << lo << ", " << hi << "]: ";
    rangeRecursive(root, lo, hi, recCount);
    cout << "\nComparisons (recursive): " << recCount << "\n";
    cout << "Iterative range [" << lo << ", " << hi << "]: ";
    rangeIterative(root, lo, hi, itCount);
    cout << "\nComparisons (iterative): " << itCount << "\n";
    return 0;
}
