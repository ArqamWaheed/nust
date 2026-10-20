#include <iostream>
#include <string>
#include <cctype>
using namespace std;

struct Node {
    char data;
    Node* left;
    Node* right;

    Node(char c) {
        data = c;
        left = nullptr;
        right = nullptr;
    }
};

Node* root = nullptr;
string treeString = "a(b(d,e),c(,f(g,)))";

// array based stack of node pointers, used for inorder and postorder
struct Stack {
    Node* items[100];
    int top = -1;

    bool isEmpty() {
        return top == -1;
    }

    bool push(Node* n) {
        if (top == 99)
            return false;
        items[++top] = n;
        return true;
    }

    Node* pop() {
        if (isEmpty())
            return nullptr;
        return items[top--];
    }

    Node* peek() {
        if (isEmpty())
            return nullptr;
        return items[top];
    }
};

// ---------- 1. build the tree from the string ----------

// i walks through the string, an empty slot before ',' or ')' gives a null child
Node* parse(const string &s, int &i) {
    if (i >= (int)s.size() || s[i] == ',' || s[i] == ')')
        return nullptr;

    Node* fresh = new Node(s[i]);
    i++;

    if (i < (int)s.size() && s[i] == '(') {
        i++;                        // skip '('
        fresh->left = parse(s, i);
        i++;                        // skip ','
        fresh->right = parse(s, i);
        i++;                        // skip ')'
    }
    return fresh;
}

Node* buildTree(const string &s) {
    int i = 0;
    return parse(s, i);
}

void destroyTree(Node* n) {
    if (n == nullptr)
        return;
    destroyTree(n->left);
    destroyTree(n->right);
    delete n;
}

// walks the tree and writes it back in bracket form, used to check the build
string toTreeString(Node* n) {
    if (n == nullptr)
        return "";

    string s(1, n->data);
    if (n->left != nullptr || n->right != nullptr)
        s += "(" + toTreeString(n->left) + "," + toTreeString(n->right) + ")";
    return s;
}

// ---------- 2. preorder (recursive) ----------

void preorder(Node* n) {
    if (n == nullptr)
        return;
    cout << n->data << " ";
    preorder(n->left);
    preorder(n->right);
}

// ---------- 3. inorder (iterative, stack) ----------

void inorderIterative() {
    Stack st;
    Node* cur = root;

    while (cur != nullptr || !st.isEmpty()) {
        // go as far left as possible
        while (cur != nullptr) {
            st.push(cur);
            cur = cur->left;
        }
        cur = st.pop();
        cout << cur->data << " ";
        cur = cur->right;
    }
}

// ---------- 4. postorder (iterative, one stack) ----------

// lastVisited stops a node from being printed before its right subtree
void postorderIterative() {
    Stack st;
    Node* cur = root;
    Node* lastVisited = nullptr;

    while (cur != nullptr || !st.isEmpty()) {
        if (cur != nullptr) {
            st.push(cur);
            cur = cur->left;
        }
        else {
            Node* top = st.peek();
            if (top->right != nullptr && lastVisited != top->right) {
                cur = top->right;
            }
            else {
                cout << top->data << " ";
                lastVisited = st.pop();
            }
        }
    }
}

// ---------- 5. validation without building the tree ----------

// tree  -> label | label '(' child ',' child ')'
// child -> tree | nothing        ("(,)" is not allowed)
bool checkTree(const string &s, int &i, string &err);

bool checkChild(const string &s, int &i, string &err, bool &present) {
    present = false;
    if (i < (int)s.size() && (s[i] == ',' || s[i] == ')'))
        return true;
    present = true;
    return checkTree(s, i, err);
}

bool checkTree(const string &s, int &i, string &err) {
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

bool isValidTreeString(const string &s, string &err) {
    // first pass: brackets must balance
    int depth = 0;
    for (int k = 0; k < (int)s.size(); k++) {
        if (s[k] == '(')
            depth++;
        else if (s[k] == ')')
            depth--;

        if (depth < 0) {
            err = "unmatched ')' at position " + to_string(k);
            return false;
        }
    }
    if (depth != 0) {
        err = "unbalanced parentheses";
        return false;
    }

    // second pass: children in the right places
    int i = 0;
    if (!checkTree(s, i, err))
        return false;
    if (i != (int)s.size()) {
        err = "extra characters after position " + to_string(i);
        return false;
    }
    return true;
}

// ---------- 6. height and depth ----------

// height in edges: a leaf is 0, an empty tree is -1
int height(Node* n) {
    if (n == nullptr)
        return -1;
    int l = height(n->left);
    int r = height(n->right);
    return 1 + (l > r ? l : r);
}

// depth is passed down, root starts at 0
void printDepths(Node* n, int depth) {
    if (n == nullptr)
        return;
    cout << "Node " << n->data << ": depth " << depth << ", height " << height(n) << endl;
    printDepths(n->left, depth + 1);
    printDepths(n->right, depth + 1);
}

// ---------- menu ----------

void showTraversals() {
    cout << "Tree      : " << toTreeString(root) << endl;
    cout << "Preorder  : ";
    preorder(root);
    cout << endl;
    cout << "Inorder   : ";
    inorderIterative();
    cout << endl;
    cout << "Postorder : ";
    postorderIterative();
    cout << endl;
}

string readTreeString() {
    string s;
    cout << "Enter tree string: ";
    cin >> s;
    return s;
}

void showMenu() {
    cout << endl;
    cout << "1.Load tree  2.Traversals  3.Height/Depth  4.Validate  5.Exit" << endl;
    cout << "Enter choice: ";
}

int main() {
    int choice;
    string s, err;
    bool running = true;

    root = buildTree(treeString);
    cout << "Tree loaded: " << treeString << endl;

    while (running) {
        showMenu();
        if (!(cin >> choice)) {
            if (cin.eof())
                break;
            cin.clear();
            cin.ignore(1000, '\n');
            cout << "Invalid choice" << endl;
            continue;
        }

        switch (choice) {
            case 1:
                s = readTreeString();
                if (!isValidTreeString(s, err)) {
                    cout << "Invalid tree string: " << err << endl;
                    break;
                }
                destroyTree(root);
                treeString = s;
                root = buildTree(treeString);
                cout << "Tree loaded: " << treeString << endl;
                showTraversals();
                break;

            case 2:
                showTraversals();
                break;

            case 3:
                cout << "Height of tree: " << height(root) << endl;
                printDepths(root, 0);
                break;

            case 4:
                s = readTreeString();
                if (isValidTreeString(s, err))
                    cout << s << " is valid" << endl;
                else
                    cout << s << " is invalid: " << err << endl;
                break;

            case 5:
                running = false;
                break;

            default:
                cout << "Invalid choice" << endl;
        }
    }

    destroyTree(root);
    cout << "Goodbye" << endl;
}
