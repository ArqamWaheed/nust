#include <iostream>
using namespace std;

struct Node {
    int id;
    int cost;
    Node* left;
    Node* right;
    Node(int i, int c) {
        id = i;
        cost = c;
        left = nullptr;
        right = nullptr;
    }
};

Node* insert(Node* root, int id, int cost) {
    if (root == nullptr)
        return new Node(id, cost);
    if (cost < root->cost)
        root->left = insert(root->left, id, cost);
    else
        root->right = insert(root->right, id, cost);
    return root;
}

// ---------- Part A: downward paths ----------
Node* path[50];
int plen = 0;
int pathsFound = 0;

// extend the path downwards from n, printing every prefix-end that sums to B
void descend(Node* n, int sum, int B) {
    if (n == nullptr)
        return;
    path[plen++] = n;                 // push
    sum += n->cost;
    if (sum == B) {
        pathsFound++;
        cout << "  ";
        for (int i = 0; i < plen; i++)
            cout << "S" << path[i]->id << "($" << path[i]->cost << ")"
                 << (i + 1 < plen ? " -> " : "");
        cout << "  = " << sum << endl;
    }
    descend(n->left, sum, B);
    descend(n->right, sum, B);
    plen--;                           // pop
}

// every node is a possible starting point
void allStarts(Node* n, int B) {
    if (n == nullptr)
        return;
    descend(n, 0, B);
    allStarts(n->left, B);
    allStarts(n->right, B);
}

// ---------- Part B: subsets ----------
Node* nodes[50];
int cnt = 0;
Node* chosen[50];
int clen = 0;
int subsetsFound = 0;
int subsetCalls = 0;
int subsetPruned = 0;

// inorder gives the nodes in increasing cost
void collect(Node* n) {
    if (n == nullptr)
        return;
    collect(n->left);
    nodes[cnt++] = n;
    collect(n->right);
}

void subsets(int idx, int sum, int B) {
    subsetCalls++;
    if (sum == B) {
        subsetsFound++;
        cout << "  {";
        for (int i = 0; i < clen; i++)
            cout << "S" << chosen[i]->id << "($" << chosen[i]->cost << ")"
                 << (i + 1 < clen ? ", " : "");
        cout << "}" << endl;
        return;
    }
    for (int i = idx; i < cnt; i++) {
        // nodes are sorted, so this and every later (larger) cost overshoots B
        if (sum + nodes[i]->cost > B) {
            subsetPruned++;
            break;
        }
        chosen[clen++] = nodes[i];
        subsets(i + 1, sum + nodes[i]->cost, B);
        clen--;
    }
}

void run(Node* root, int B) {
    cout << "Target budget B = " << B << endl;
    pathsFound = 0;
    cout << "Part A - downward paths:" << endl;
    allStarts(root, B);
    if (pathsFound == 0)
        cout << "  none" << endl;

    cnt = 0;
    clen = 0;
    subsetsFound = 0;
    subsetCalls = 0;
    subsetPruned = 0;
    collect(root);
    cout << "Part B - subsets of the whole BST:" << endl;
    subsets(0, 0, B);
    if (subsetsFound == 0)
        cout << "  none" << endl;
    cout << "  " << subsetsFound << " subset(s), " << subsetCalls
         << " calls, " << subsetPruned << " prunes" << endl << endl;
}

int main() {
    int costs[] = {50, 30, 70, 20, 40, 60, 80, 10};
    Node* root = nullptr;
    for (int i = 0; i < 8; i++)
        root = insert(root, i + 1, costs[i]);
    cout << "BST costs inserted: 50 30 70 20 40 60 80 10" << endl << endl;
    run(root, 90);
    run(root, 120);
    run(root, 7);
    return 0;
}
