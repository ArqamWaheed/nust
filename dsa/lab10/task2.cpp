#include <iostream>
using namespace std;

const int MAXK = 20;

// explicit operation stack
struct OpStack {
    int op[MAXK];
    int top;
    OpStack() { top = -1; }
    void push(int o) { op[++top] = o; }
    void pop() { top--; }
};

// operation codes
const int ADD3 = 0, MUL2 = 1, SUB5 = 2, DIV2 = 3;
const char* names[] = {"+3", "*2", "-5", "/2"};

int found = 0;
int calls = 0;

// returns false if the operation is not allowed on v, else sets out
bool apply(int op, int v, int& out) {
    if (op == ADD3) out = v + 3;
    else if (op == MUL2) out = v * 2;
    else if (op == SUB5) out = v - 5;
    else {
        if (v % 2 != 0) return false;   // only exact halving
        out = v / 2;
    }
    return true;
}

void search(int value, int target, int k, int mmax, OpStack& st) {
    calls++;
    if (value == target) {
        found++;
        cout << found << ") ";
        if (st.top < 0)
            cout << "(no operations)";
        for (int i = 0; i <= st.top; i++)
            cout << names[st.op[i]] << " ";
        cout << "  [" << st.top + 1 << " ops]" << endl;
    }
    if (st.top + 1 == k)
        return;
    for (int op = 0; op < 4; op++) {
        int next;
        if (!apply(op, value, next))
            continue;
        if (next < 0 || next > mmax)    // prune
            continue;
        st.push(op);
        search(next, target, k, mmax, st);
        st.pop();                       // undo
    }
}

void run(int start, int target, int k, int mmax) {
    OpStack st;
    found = 0;
    calls = 0;
    cout << "start=" << start << " target=" << target << " K=" << k
         << " Mmax=" << mmax << " ops: +3 *2 -5 /2" << endl;
    search(start, target, k, mmax, st);
    if (found == 0)
        cout << "No sequence found." << endl;
    cout << found << " sequence(s), " << calls << " recursive calls" << endl << endl;
}

int main() {
    run(2, 10, 4, 100);
    run(5, 5, 2, 50);
    run(3, 100, 3, 200);
    return 0;
}
