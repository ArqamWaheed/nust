#include <iostream>
#include <string>
#include <cmath>
using namespace std;

struct StrNode {
    string data;
    StrNode* next;

    StrNode(string d, StrNode* n) {
        data = d;
        next = n;
    }
};

class StrStack {
    StrNode* head;

public:
    StrStack() {
        head = nullptr;
    }

    ~StrStack() {
        while (!isEmpty())
            pop();
    }

    bool isEmpty() {
        return head == nullptr;
    }

    void push(string x) {
        head = new StrNode(x, head);
    }

    string pop() {
        if (isEmpty())
            throw string("Invalid expression");
        StrNode* doomed = head;
        string x = doomed->data;
        head = head->next;
        delete doomed;
        return x;
    }

    string top() {
        if (isEmpty())
            throw string("Invalid expression");
        return head->data;
    }
};

struct NumNode {
    double data;
    NumNode* next;

    NumNode(double d, NumNode* n) {
        data = d;
        next = n;
    }
};

class NumStack {
    NumNode* head;

public:
    NumStack() {
        head = nullptr;
    }

    ~NumStack() {
        while (!isEmpty())
            pop();
    }

    bool isEmpty() {
        return head == nullptr;
    }

    void push(double x) {
        head = new NumNode(x, head);
    }

    double pop() {
        if (isEmpty())
            throw string("Invalid expression");
        NumNode* doomed = head;
        double x = doomed->data;
        head = head->next;
        delete doomed;
        return x;
    }
};

string nextToken(string expr, int& i) {
    while (i < (int)expr.size() && expr[i] == ' ')
        i++;
    if (i >= (int)expr.size())
        return "";

    string tok;
    if (isdigit(expr[i]) || expr[i] == '.') {
        while (i < (int)expr.size() && (isdigit(expr[i]) || expr[i] == '.'))
            tok += expr[i++];
    }
    else
        tok = expr[i++];
    return tok;
}

bool isOperator(string t) {
    return t == "+" || t == "-" || t == "*" || t == "/" || t == "^";
}

bool isOperand(string t) {
    return isalnum(t[0]) || t[0] == '.';
}

int prec(string op) {
    if (op == "^")
        return 3;
    if (op == "*" || op == "/")
        return 2;
    if (op == "+" || op == "-")
        return 1;
    return 0;
}

bool shouldPop(string top, string op) {
    if (top == "(")
        return false;
    if (prec(top) > prec(op))
        return true;
    return prec(top) == prec(op) && op != "^";
}

double toNumber(string t) {
    if (!isdigit(t[0]) && t[0] != '.')
        throw string("Cannot evaluate variable " + t);
    return stod(t);
}

double apply(string op, double a, double b) {
    if (op == "+")
        return a + b;
    if (op == "-")
        return a - b;
    if (op == "*")
        return a * b;
    if (op == "/") {
        if (b == 0)
            throw string("Division by zero");
        return a / b;
    }
    return pow(a, b);
}

string infix_to_postfix(string expr) {
    StrStack ops;
    string out;
    int i = 0;
    string tok = nextToken(expr, i);

    while (tok != "") {
        if (isOperand(tok))
            out += tok + " ";
        else if (tok == "(")
            ops.push(tok);
        else if (tok == ")") {
            while (ops.top() != "(")
                out += ops.pop() + " ";
            ops.pop();
        }
        else if (isOperator(tok)) {
            while (!ops.isEmpty() && shouldPop(ops.top(), tok))
                out += ops.pop() + " ";
            ops.push(tok);
        }
        else
            throw string("Invalid character " + tok);
        tok = nextToken(expr, i);
    }

    while (!ops.isEmpty()) {
        string op = ops.pop();
        if (op == "(")
            throw string("Mismatched parentheses");
        out += op + " ";
    }

    if (out != "")
        out.pop_back();
    return out;
}

void reduce(StrStack& ops, StrStack& vals) {
    string op = ops.pop();
    string b = vals.pop();
    string a = vals.pop();
    vals.push(op + " " + a + " " + b);
}

string infix_to_prefix(string expr) {
    StrStack ops;
    StrStack vals;
    int i = 0;
    string tok = nextToken(expr, i);

    while (tok != "") {
        if (isOperand(tok))
            vals.push(tok);
        else if (tok == "(")
            ops.push(tok);
        else if (tok == ")") {
            while (ops.top() != "(")
                reduce(ops, vals);
            ops.pop();
        }
        else if (isOperator(tok)) {
            while (!ops.isEmpty() && shouldPop(ops.top(), tok))
                reduce(ops, vals);
            ops.push(tok);
        }
        else
            throw string("Invalid character " + tok);
        tok = nextToken(expr, i);
    }

    while (!ops.isEmpty()) {
        if (ops.top() == "(")
            throw string("Mismatched parentheses");
        reduce(ops, vals);
    }

    string result = vals.pop();
    if (!vals.isEmpty())
        throw string("Invalid expression");
    return result;
}

string postfix_to_infix(string expr) {
    StrStack vals;
    int i = 0;
    string tok = nextToken(expr, i);

    while (tok != "") {
        if (isOperand(tok))
            vals.push(tok);
        else if (isOperator(tok)) {
            string b = vals.pop();
            string a = vals.pop();
            vals.push("(" + a + " " + tok + " " + b + ")");
        }
        else
            throw string("Invalid character " + tok);
        tok = nextToken(expr, i);
    }

    string result = vals.pop();
    if (!vals.isEmpty())
        throw string("Invalid expression");
    return result;
}

double evaluate_postfix(string expr) {
    NumStack vals;
    int i = 0;
    string tok = nextToken(expr, i);

    while (tok != "") {
        if (isOperand(tok))
            vals.push(toNumber(tok));
        else if (isOperator(tok)) {
            double b = vals.pop();
            double a = vals.pop();
            vals.push(apply(tok, a, b));
        }
        else
            throw string("Invalid character " + tok);
        tok = nextToken(expr, i);
    }

    double result = vals.pop();
    if (!vals.isEmpty())
        throw string("Invalid expression");
    return result;
}

double evaluate_prefix(string expr) {
    StrStack tokens;
    NumStack vals;
    int i = 0;
    string tok = nextToken(expr, i);

    while (tok != "") {
        tokens.push(tok);
        tok = nextToken(expr, i);
    }

    while (!tokens.isEmpty()) {
        tok = tokens.pop();
        if (isOperand(tok))
            vals.push(toNumber(tok));
        else if (isOperator(tok)) {
            double a = vals.pop();
            double b = vals.pop();
            vals.push(apply(tok, a, b));
        }
        else
            throw string("Invalid character " + tok);
    }

    double result = vals.pop();
    if (!vals.isEmpty())
        throw string("Invalid expression");
    return result;
}

void showMenu() {
    cout << endl;
    cout << "1.Infix to Postfix  2.Infix to Prefix  3.Postfix to Infix" << endl;
    cout << "4.Evaluate Postfix  5.Evaluate Prefix  6.Exit" << endl;
    cout << "Enter choice: ";
}

int main() {
    int choice;
    string expr;
    bool running = true;

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

        if (choice == 6) {
            running = false;
            continue;
        }
        if (choice < 1 || choice > 6) {
            cout << "Invalid choice" << endl;
            continue;
        }

        cout << "Enter expression: ";
        cin.ignore(1000, '\n');
        getline(cin, expr);

        try {
            switch (choice) {
                case 1: {
                    string r = infix_to_postfix(expr);
                    cout << "Postfix: " << r << endl;
                    break;
                }

                case 2: {
                    string r = infix_to_prefix(expr);
                    cout << "Prefix: " << r << endl;
                    break;
                }

                case 3: {
                    string r = postfix_to_infix(expr);
                    cout << "Infix: " << r << endl;
                    break;
                }

                case 4: {
                    double r = evaluate_postfix(expr);
                    cout << "Result: " << r << endl;
                    break;
                }

                case 5: {
                    double r = evaluate_prefix(expr);
                    cout << "Result: " << r << endl;
                    break;
                }
            }
        }
        catch (string err) {
            cout << "Error: " << err << endl;
        }
    }

    cout << "Exiting" << endl;
}
