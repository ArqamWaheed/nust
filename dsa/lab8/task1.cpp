#include <iostream>
#include <string>
#include <stdexcept>
using namespace std;

struct Node {
    char data;
    Node* left;
    Node* right;
    Node(char c) { data = c; left = right = nullptr; }
};

// array based stack, used instead of recursion for inorder and postorder
template <typename T>
class Stack {
    T* items;
    int capacity;
    int topIndex;

public:
    Stack(int cap = 100) {
        capacity = cap;
        items = new T[capacity];
        topIndex = -1;
    }
    ~Stack() { delete[] items; }

    bool empty() { return topIndex == -1; }
    void push(T x) {
        if (topIndex == capacity - 1)
            throw runtime_error("stack overflow");
        items[++topIndex] = x;
    }
    T pop() {
        if (empty())
            throw runtime_error("stack underflow");
        return items[topIndex--];
    }
    T peek() {
        if (empty())
            throw runtime_error("stack underflow");
        return items[topIndex];
    }
};

// ---------- 5. validation without building the tree ----------
// grammar:  tree  -> letter | letter '(' child ',' child ')'
//           child -> tree | empty
bool checkTree(const string& s, int& i, string& err);

bool checkChild(const string& s, int& i, string& err, bool& present) {
    present = false;
    if (i < (int)s.size() && (s[i] == ',' || s[i] == ')'))
        return true;
    present = true;
    return checkTree(s, i, err);
}

bool checkTree(const string& s, int& i, string& err) {
    if (i >= (int)s.size() || !isalnum(s[i])) {
        err = "expected a node label at position " + to_string(i);
        return false;
    }
    i++;
    if (i >= (int)s.size() || s[i] != '(')
        return true;
    i++;
    bool hasLeft, hasRight;
    if (!checkChild(s, i, err, hasLeft))
        return false;
    if (i >= (int)s.size() || s[i] != ',') {
        err = "expected ',' between children at position " + to_string(i);
        return false;
    }
    i++;
    if (!checkChild(s, i, err, hasRight))
        return false;
    if (i >= (int)s.size() || s[i] != ')') {
        err = "expected ')' at position " + to_string(i);
        return false;
    }
    if (!hasLeft && !hasRight) {
        err = "empty brackets '(,)' at position " + to_string(i - 2);
        return false;
    }
    i++;
    return true;
}

bool isValidTreeString(const string& s, string& err) {
    // first pass: brackets must balance
    int depth = 0;
    for (int k = 0; k < (int)s.size(); k++) {
        if (s[k] == '(') depth++;
        else if (s[k] == ')') depth--;
        if (depth < 0) {
            err = "unmatched ')' at position " + to_string(k);
            return false;
        }
    }
    if (depth != 0) {
        err = "unbalanced parentheses";
        return false;
    }
    // second pass: correct child placement
    int i = 0;
    if (!checkTree(s, i, err))
        return false;
    if (i != (int)s.size()) {
        err = "extra characters after position " + to_string(i);
        return false;
    }
    return true;
}

// ---------- 1. build the tree from the string ----------
Node* parse(const string& s, int& i) {
    if (i >= (int)s.size() || s[i] == ',' || s[i] == ')')
        return nullptr;
    Node* n = new Node(s[i++]);
    if (i < (int)s.size() && s[i] == '(') {
        i++;
        n->left = parse(s, i);
        i++; // skip ','
        n->right = parse(s, i);
        i++; // skip ')'
    }
    return n;
}

Node* buildTree(const string& s) {
    int i = 0;
    return parse(s, i);
}

void destroy(Node* n) {
    if (!n) return;
    destroy(n->left);
    destroy(n->right);
    delete n;
}

// ---------- 2. preorder (recursive) ----------
void preorder(Node* n, string& out) {
    if (!n) return;
    out += n->data;
    out += ' ';
    preorder(n->left, out);
    preorder(n->right, out);
}

// rebuilds the bracket form by walking the tree in preorder
string toTreeString(Node* n) {
    if (!n) return "";
    string s(1, n->data);
    if (n->left || n->right)
        s += "(" + toTreeString(n->left) + "," + toTreeString(n->right) + ")";
    return s;
}

// ---------- 3. inorder (iterative, stack) ----------
string inorderIterative(Node* root) {
    string out;
    Stack<Node*> st;
    Node* cur = root;
    while (cur || !st.empty()) {
        while (cur) {          // go as far left as possible
            st.push(cur);
            cur = cur->left;
        }
        cur = st.pop();
        out += cur->data;
        out += ' ';
        cur = cur->right;
    }
    return out;
}

// ---------- 4. postorder (iterative, one stack) ----------
string postorderIterative(Node* root) {
    string out;
    Stack<Node*> st;
    Node* cur = root;
    Node* lastVisited = nullptr;
    while (cur || !st.empty()) {
        if (cur) {
            st.push(cur);
            cur = cur->left;
        } else {
            Node* top = st.peek();
            // right subtree exists and has not been printed yet
            if (top->right && lastVisited != top->right) {
                cur = top->right;
            } else {
                out += top->data;
                out += ' ';
                lastVisited = st.pop();
            }
        }
    }
    return out;
}

// ---------- 6. height and depth ----------
// height counted in edges: a single node has height 0, an empty tree -1
int height(Node* n) {
    if (!n) return -1;
    int l = height(n->left);
    int r = height(n->right);
    return 1 + (l > r ? l : r);
}

void printDepths(Node* n, int depth) {
    if (!n) return;
    cout << "    node " << n->data << " : depth " << depth << ", height " << height(n) << endl;
    printDepths(n->left, depth + 1);
    printDepths(n->right, depth + 1);
}

// ---------- menu ----------
void showTraversals(Node* root) {
    string pre;
    preorder(root, pre);
    cout << "  Tree form            : " << toTreeString(root) << endl;
    cout << "  Preorder  (recursive): " << pre << endl;
    cout << "  Inorder   (stack)    : " << inorderIterative(root) << endl;
    cout << "  Postorder (stack)    : " << postorderIterative(root) << endl;
}

void showHeight(Node* root) {
    cout << "  Height of tree = " << height(root) << " (edges on longest root-to-leaf path)" << endl;
    printDepths(root, 0);
}

int main() {
    string treeStr = "a(b(d,e),c(,f(g,)))";
    string err;
    Node* root = buildTree(treeStr);
    cout << "Loaded tree: " << treeStr << endl;

    int choice = -1;
    while (choice != 0) {
        cout << "\n[1] Load tree string  [2] Traversals  [3] Height/depth  [4] Validate string  [0] Exit" << endl;
        cout << "Choice: ";
        if (!(cin >> choice)) break;

        if (choice == 1 || choice == 4) {
            string s;
            cout << "Tree string: ";
            cin >> s;
            bool ok = isValidTreeString(s, err);
            if (choice == 4) {
                cout << "  " << s << " -> " << (ok ? "VALID" : "INVALID (" + err + ")") << endl;
            } else if (!ok) {
                cout << "  Error : " << err << ", tree not changed" << endl;
            } else {
                destroy(root);
                root = buildTree(s);
                cout << "  Tree built from " << s << endl;
                showTraversals(root);
            }
        } else if (choice == 2) {
            showTraversals(root);
        } else if (choice == 3) {
            showHeight(root);
        } else if (choice != 0) {
            cout << "  Invalid choice" << endl;
        }
    }

    destroy(root);
    cout << "Goodbye" << endl;
}
