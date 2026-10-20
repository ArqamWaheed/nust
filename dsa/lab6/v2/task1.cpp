#include <iostream>
#include <string>
#include <cmath>
#include <stdexcept>
using namespace std;

const int MAX = 100;

class StringStack {
    string items[MAX];
    int topIndex;

public:
    StringStack() { topIndex = -1; }

    bool empty() { return topIndex == -1; }

    void push(string s) {
        if (topIndex == MAX - 1)
            throw runtime_error("stack overflow");
        items[++topIndex] = s;
    }

    string pop() {
        if (empty())
            throw runtime_error("malformed expression");
        return items[topIndex--];
    }

    string peek() {
        if (empty())
            throw runtime_error("malformed expression");
        return items[topIndex];
    }
};

class DoubleStack {
    double items[MAX];
    int topIndex;

public:
    DoubleStack() { topIndex = -1; }

    bool empty() { return topIndex == -1; }

    void push(double d) {
        if (topIndex == MAX - 1)
            throw runtime_error("stack overflow");
        items[++topIndex] = d;
    }

    double pop() {
        if (empty())
            throw runtime_error("malformed expression");
        return items[topIndex--];
    }
};

bool isOp(string t) {
    return t == "+" || t == "-" || t == "*" || t == "/" || t == "^";
}

bool isValue(string t) {
    return isdigit(t[0]) || t[0] == '.' || isalpha(t[0]);
}

int precedence(string op) {
    if (op == "^") return 3;
    if (op == "*" || op == "/") return 2;
    if (op == "+" || op == "-") return 1;
    return 0;
}

int tokenize(string expr, string tokens[]) {
    int n = 0;
    int i = 0;
    while (i < (int)expr.length()) {
        char c = expr[i];
        if (c == ' ') {
            i++;
        }
        else if (isdigit(c) || c == '.') {
            string num;
            while (i < (int)expr.length() && (isdigit(expr[i]) || expr[i] == '.'))
                num += expr[i++];
            tokens[n++] = num;
        }
        else if (isalpha(c) || c == '(' || c == ')' || isOp(string(1, c))) {
            tokens[n++] = string(1, c);
            i++;
        }
        else {
            throw runtime_error(string("unknown symbol '") + c + "'");
        }
        if (n == MAX)
            throw runtime_error("expression too long");
    }
    return n;
}

string join(string tokens[], int n) {
    string result;
    for (int i = 0; i < n; i++) {
        if (i > 0)
            result += " ";
        result += tokens[i];
    }
    return result;
}

int shunt(string in[], int n, string out[], bool reversed) {
    StringStack ops;
    int m = 0;

    for (int i = 0; i < n; i++) {
        string t = in[i];
        if (isValue(t)) {
            out[m++] = t;
        }
        else if (t == "(") {
            ops.push(t);
        }
        else if (t == ")") {
            while (!ops.empty() && ops.peek() != "(")
                out[m++] = ops.pop();
            if (ops.empty())
                throw runtime_error("unbalanced parentheses");
            ops.pop();
        }
        else {
            while (!ops.empty() && ops.peek() != "(") {
                int top = precedence(ops.peek());
                int cur = precedence(t);
                bool rightAssoc = (t == "^");
                bool popIt;
                if (reversed)
                    popIt = top > cur || (top == cur && rightAssoc);
                else
                    popIt = top > cur || (top == cur && !rightAssoc);
                if (!popIt)
                    break;
                out[m++] = ops.pop();
            }
            ops.push(t);
        }
    }

    while (!ops.empty()) {
        if (ops.peek() == "(")
            throw runtime_error("unbalanced parentheses");
        out[m++] = ops.pop();
    }
    return m;
}

string infix_to_postfix(string expr) {
    string tokens[MAX], out[MAX];
    int n = tokenize(expr, tokens);
    int m = shunt(tokens, n, out, false);
    return join(out, m);
}

string infix_to_prefix(string expr) {
    string tokens[MAX], rev[MAX], out[MAX], pre[MAX];
    int n = tokenize(expr, tokens);

    for (int i = 0; i < n; i++) {
        string t = tokens[n - 1 - i];
        if (t == "(")
            rev[i] = ")";
        else if (t == ")")
            rev[i] = "(";
        else
            rev[i] = t;
    }

    int m = shunt(rev, n, out, true);
    for (int i = 0; i < m; i++)
        pre[i] = out[m - 1 - i];
    return join(pre, m);
}

string postfix_to_infix(string expr) {
    string tokens[MAX];
    int n = tokenize(expr, tokens);
    StringStack st;

    for (int i = 0; i < n; i++) {
        if (isValue(tokens[i])) {
            st.push(tokens[i]);
        }
        else if (isOp(tokens[i])) {
            string right = st.pop();
            string left = st.pop();
            st.push("(" + left + " " + tokens[i] + " " + right + ")");
        }
        else {
            throw runtime_error("parentheses are not allowed in postfix");
        }
    }

    string result = st.pop();
    if (!st.empty())
        throw runtime_error("too many operands");
    return result;
}

double calculate(double a, double b, string op) {
    if (op == "+") return a + b;
    if (op == "-") return a - b;
    if (op == "*") return a * b;
    if (op == "^") return pow(a, b);
    if (b == 0)
        throw runtime_error("division by zero");
    return a / b;
}

double numberOf(string t) {
    if (isalpha(t[0]))
        throw runtime_error("variable '" + t + "' has no value");
    return stod(t);
}

double evaluate_postfix(string expr) {
    string tokens[MAX];
    int n = tokenize(expr, tokens);
    DoubleStack st;

    for (int i = 0; i < n; i++) {
        if (isValue(tokens[i])) {
            st.push(numberOf(tokens[i]));
        }
        else if (isOp(tokens[i])) {
            double b = st.pop();
            double a = st.pop();
            st.push(calculate(a, b, tokens[i]));
        }
        else {
            throw runtime_error("parentheses are not allowed in postfix");
        }
    }

    double result = st.pop();
    if (!st.empty())
        throw runtime_error("too many operands");
    return result;
}

double evaluate_prefix(string expr) {
    string tokens[MAX];
    int n = tokenize(expr, tokens);
    DoubleStack st;

    for (int i = n - 1; i >= 0; i--) {
        if (isValue(tokens[i])) {
            st.push(numberOf(tokens[i]));
        }
        else if (isOp(tokens[i])) {
            double a = st.pop();
            double b = st.pop();
            st.push(calculate(a, b, tokens[i]));
        }
        else {
            throw runtime_error("parentheses are not allowed in prefix");
        }
    }

    double result = st.pop();
    if (!st.empty())
        throw runtime_error("too many operands");
    return result;
}

void analyse(string infix) {
    string postfix = infix_to_postfix(infix);
    string prefix = infix_to_prefix(infix);
    cout << "  Postfix        : " << postfix << endl;
    cout << "  Prefix         : " << prefix << endl;
    cout << "  Back to infix  : " << postfix_to_infix(postfix) << endl;
    try {
        double fromPostfix = evaluate_postfix(postfix);
        double fromPrefix = evaluate_prefix(prefix);
        cout << "  Postfix value  : " << fromPostfix << endl;
        cout << "  Prefix value   : " << fromPrefix << endl;
    }
    catch (runtime_error& e) {
        cout << "  Value          : not evaluated, " << e.what() << endl;
    }
}

int main() {
    int choice = -1;
    string line;

    while (choice != 0) {
        cout << "\n[1] Analyse infix  [2] Postfix to infix  [3] Evaluate postfix  [4] Evaluate prefix  [0] Exit" << endl;
        cout << "Choice: ";

        if (!(cin >> choice)) {
            if (cin.eof())
                break;
            cin.clear();
            cin.ignore(1000, '\n');
            choice = -1;
            cout << "Please enter a number" << endl;
            continue;
        }
        if (choice == 0)
            break;
        if (choice < 0 || choice > 4) {
            cout << "Please choose 0-4" << endl;
            continue;
        }

        cout << "Expression: ";
        cin.ignore(1000, '\n');
        getline(cin, line);

        try {
            if (choice == 1) {
                analyse(line);
            }
            else if (choice == 2) {
                string infix = postfix_to_infix(line);
                cout << "  Infix : " << infix << endl;
            }
            else {
                double value = (choice == 3) ? evaluate_postfix(line) : evaluate_prefix(line);
                cout << "  Value : " << value << endl;
            }
        }
        catch (runtime_error& e) {
            cout << "  Error : " << e.what() << endl;
        }
    }

    cout << "Goodbye" << endl;
}
