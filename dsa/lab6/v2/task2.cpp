#include <iostream>
#include <string>
using namespace std;

const int MAX = 200;

class CharStack {
    char items[MAX];
    int topIndex;

public:
    CharStack() { topIndex = -1; }
    bool empty() { return topIndex == -1; }
    bool full() { return topIndex == MAX - 1; }
    void push(char c) { items[++topIndex] = c; }
    char pop() { return items[topIndex--]; }
};

class TagStack {
    string names[MAX];
    int positions[MAX];
    int topIndex;

public:
    TagStack() { topIndex = -1; }
    bool empty() { return topIndex == -1; }
    bool full() { return topIndex == MAX - 1; }
    int size() { return topIndex + 1; }

    void push(string name, int pos) {
        topIndex++;
        names[topIndex] = name;
        positions[topIndex] = pos;
    }

    void pop() { topIndex--; }
    string topName() { return names[topIndex]; }
    int topPos() { return positions[topIndex]; }
    string nameBelowTop() { return names[topIndex - 1]; }
};

struct MarkupResult {
    bool valid;
    string errors[MAX];
    int errorCount;
};

char matching(char close) {
    if (close == ')') return '(';
    if (close == ']') return '[';
    return '{';
}

bool isValidBrackets(string s) {
    CharStack st;
    for (int i = 0; i < (int)s.length(); i++) {
        char c = s[i];
        if (c == '(' || c == '[' || c == '{') {
            if (st.full())
                return false;
            st.push(c);
        }
        else if (c == ')' || c == ']' || c == '}') {
            if (st.empty() || st.pop() != matching(c))
                return false;
        }
    }
    return st.empty();
}

string lower(string s) {
    for (int i = 0; i < (int)s.length(); i++)
        s[i] = tolower(s[i]);
    return s;
}

bool isVoidTag(string name) {
    string voids[] = {"br", "hr", "img", "input", "meta", "link"};
    for (int i = 0; i < 6; i++)
        if (name == voids[i])
            return true;
    return false;
}

void report(MarkupResult& r, string msg) {
    if (r.errorCount < MAX)
        r.errors[r.errorCount++] = msg;
}

MarkupResult validate_markup(string s) {
    MarkupResult r;
    r.errorCount = 0;
    TagStack st;
    int i = 0;

    while (i < (int)s.length()) {
        if (s[i] != '<') {
            i++;
            continue;
        }

        int start = i;
        int end = s.find('>', i);
        if (end == -1) {
            report(r, "char " + to_string(start) + ": '<' has no closing '>'");
            break;
        }
        string body = s.substr(start + 1, end - start - 1);
        i = end + 1;

        bool isClosing = body.length() > 0 && body[0] == '/';
        bool selfClosing = body.length() > 0 && body[body.length() - 1] == '/';
        if (isClosing)
            body = body.substr(1);

        string name;
        int k = 0;
        while (k < (int)body.length() && isalnum(body[k]))
            name += body[k++];
        name = lower(name);

        if (name == "") {
            report(r, "char " + to_string(start) + ": tag has no name");
            continue;
        }

        if (isClosing) {
            if (isVoidTag(name)) {
                report(r, "char " + to_string(start) + ": <" + name + "> never needs a closing tag");
            }
            else if (st.empty()) {
                report(r, "char " + to_string(start) + ": </" + name + "> has no opening tag");
            }
            else if (st.topName() == name) {
                st.pop();
            }
            else {
                report(r, "char " + to_string(start) + ": expected </" + st.topName() + "> but found </" + name + ">");
                if (st.size() > 1 && st.nameBelowTop() == name) {
                    st.pop();
                    st.pop();
                }
            }
        }
        else if (!selfClosing && !isVoidTag(name)) {
            if (st.full()) {
                report(r, "too many nested tags");
                break;
            }
            st.push(name, start);
        }
    }

    while (!st.empty()) {
        report(r, "char " + to_string(st.topPos()) + ": <" + st.topName() + "> is never closed");
        st.pop();
    }

    r.valid = (r.errorCount == 0);
    return r;
}

int main() {
    int choice = -1;
    string line;

    while (choice != 0) {
        cout << "\n[1] Check brackets  [2] Check HTML/XML markup  [0] Exit" << endl;
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
        if (choice != 1 && choice != 2) {
            cout << "Please choose 0-2" << endl;
            continue;
        }

        cout << "Input: ";
        cin.ignore(1000, '\n');
        getline(cin, line);

        if (choice == 1) {
            cout << "  " << (isValidBrackets(line) ? "true  (balanced)" : "false (not balanced)") << endl;
        }
        else {
            MarkupResult r = validate_markup(line);
            if (r.valid) {
                cout << "  true, no errors" << endl;
            }
            else {
                cout << "  false, " << r.errorCount << " error(s)" << endl;
                for (int j = 0; j < r.errorCount; j++)
                    cout << "    - " << r.errors[j] << endl;
            }
        }
    }

    cout << "Goodbye" << endl;
}
