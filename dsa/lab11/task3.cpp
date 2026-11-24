#include <iostream>
#include <string>
using namespace std;

struct Node {
    int key;
    int height;
    Node* left;
    Node* right;
    Node(int k) {
        key = k;
        height = 1;
        left = nullptr;
        right = nullptr;
    }
};

string rotations = "";   // what the last operation had to do to heal the tree

int height(Node* n) {
    return n == nullptr ? 0 : n->height;
}

int bigger(int a, int b) {
    return a > b ? a : b;
}

void update(Node* n) {
    n->height = 1 + bigger(height(n->left), height(n->right));
}

int balance(Node* n) {
    return n == nullptr ? 0 : height(n->left) - height(n->right);
}

Node* rotateRight(Node* y) {
    Node* x = y->left;
    y->left = x->right;
    x->right = y;
    update(y);
    update(x);
    return x;
}

Node* rotateLeft(Node* x) {
    Node* y = x->right;
    x->right = y->left;
    y->left = x;
    update(x);
    update(y);
    return y;
}

// only rotates when |balance| > 1, otherwise the node is returned as it is
Node* rebalance(Node* n) {
    update(n);
    int b = balance(n);
    if (b > 1) {
        if (balance(n->left) < 0) {
            rotations += "LR at " + to_string(n->key) + "  ";
            n->left = rotateLeft(n->left);
        } else
            rotations += "LL at " + to_string(n->key) + "  ";
        return rotateRight(n);
    }
    if (b < -1) {
        if (balance(n->right) > 0) {
            rotations += "RL at " + to_string(n->key) + "  ";
            n->right = rotateRight(n->right);
        } else
            rotations += "RR at " + to_string(n->key) + "  ";
        return rotateLeft(n);
    }
    return n;
}

Node* insert(Node* root, int key) {
    if (root == nullptr)
        return new Node(key);
    if (key < root->key)
        root->left = insert(root->left, key);
    else if (key > root->key)
        root->right = insert(root->right, key);
    else
        return root;   // no duplicates
    return rebalance(root);
}

Node* remove(Node* root, int key) {
    if (root == nullptr)
        return nullptr;
    if (key < root->key)
        root->left = remove(root->left, key);
    else if (key > root->key)
        root->right = remove(root->right, key);
    else {
        if (root->left == nullptr || root->right == nullptr) {
            Node* child = root->left ? root->left : root->right;
            delete root;
            return child;
        }
        // two children: copy the inorder successor and delete it from the right subtree
        Node* s = root->right;
        while (s->left != nullptr)
            s = s->left;
        root->key = s->key;
        root->right = remove(root->right, s->key);
    }
    return rebalance(root);
}

// prints the tree as root(left,right), '-' for a missing child
void printTree(Node* n) {
    if (n == nullptr) {
        cout << "-";
        return;
    }
    cout << n->key;
    if (n->left == nullptr && n->right == nullptr)
        return;
    cout << "(";
    printTree(n->left);
    cout << ",";
    printTree(n->right);
    cout << ")";
}

// self check: every node has |balance| <= 1 and a correct height
bool isAVL(Node* n) {
    if (n == nullptr)
        return true;
    if (balance(n) > 1 || balance(n) < -1)
        return false;
    if (n->height != 1 + bigger(height(n->left), height(n->right)))
        return false;
    return isAVL(n->left) && isAVL(n->right);
}

void show(Node* root) {
    cout << "    rotations: " << (rotations == "" ? "none" : rotations) << endl;
    cout << "    tree: ";
    printTree(root);
    cout << "   height " << height(root) << (isAVL(root) ? ", balanced" : ", NOT balanced") << endl;
    rotations = "";
}

// collect up to k keys: reverse inorder gives the largest first, inorder the smallest first
void largest(Node* n, int k, int out[], int& count) {
    if (n == nullptr || count == k)
        return;
    largest(n->right, k, out, count);
    if (count < k)
        out[count++] = n->key;
    largest(n->left, k, out, count);
}

void smallest(Node* n, int k, int out[], int& count) {
    if (n == nullptr || count == k)
        return;
    smallest(n->left, k, out, count);
    if (count < k)
        out[count++] = n->key;
    smallest(n->right, k, out, count);
}

// criterion: "max" = k largest, "min" = k smallest, "sum" = sum of the k largest
int topK(Node* root, string criterion, int k, int out[]) {
    int count = 0;
    if (criterion == "min")
        smallest(root, k, out, count);
    else
        largest(root, k, out, count);
    return count;
}

void query(Node* root, string criterion, int k) {
    int out[100];
    int c = topK(root, criterion, k, out);
    cout << "top " << k << " (" << criterion << "): ";
    if (criterion == "sum") {
        int sum = 0;
        for (int i = 0; i < c; i++) {
            sum += out[i];
            cout << out[i] << (i < c - 1 ? " + " : "");
        }
        cout << " = " << sum << endl;
    } else {
        for (int i = 0; i < c; i++)
            cout << out[i] << " ";
        cout << endl;
    }
}

Node* deleteTopK(Node* root, string criterion, int k) {
    int out[100];
    int c = topK(root, criterion, k, out);
    cout << "deleting top " << k << " (" << criterion << ")" << endl;
    for (int i = 0; i < c; i++) {
        root = remove(root, out[i]);
        cout << "  delete " << out[i] << endl;
        show(root);
    }
    return root;
}

Node* updateKey(Node* root, int oldKey, int newKey) {
    root = remove(root, oldKey);
    root = insert(root, newKey);
    cout << "update " << oldKey << " -> " << newKey << endl;
    show(root);
    return root;
}

void freeTree(Node* n) {
    if (n == nullptr)
        return;
    freeTree(n->left);
    freeTree(n->right);
    delete n;
}

int main() {
    Node* root = nullptr;
    int keys[] = {10, 20, 30, 40, 50, 25, 35, 5, 4, 45, 60};
    int n = 11;
    for (int i = 0; i < n; i++) {
        root = insert(root, keys[i]);
        cout << "insert " << keys[i] << endl;
        show(root);
    }
    cout << endl;
    query(root, "max", 3);
    query(root, "min", 3);
    query(root, "sum", 3);
    cout << endl;
    root = updateKey(root, 4, 55);
    cout << endl;
    root = deleteTopK(root, "max", 4);
    cout << endl;
    root = deleteTopK(root, "min", 3);
    cout << endl;
    query(root, "max", 3);
    freeTree(root);
    return 0;
}
