#include <iostream>
#include <string>
using namespace std;

struct CharNode {
    char data;
    CharNode* next;

    CharNode(char d, CharNode* n) {
        data = d;
        next = n;
    }
};

class CharStack {
    CharNode* head;

public:
    CharStack() {
        head = nullptr;
    }

    ~CharStack() {
        while (!isEmpty())
            pop();
    }

    bool isEmpty() {
        return head == nullptr;
    }

    void push(char x) {
        head = new CharNode(x, head);
    }

    char pop() {
        CharNode* doomed = head;
        char x = doomed->data;
        head = head->next;
        delete doomed;
        return x;
    }

    char top() {
        return head->data;
    }
};

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
        StrNode* doomed = head;
        string x = doomed->data;
        head = head->next;
        delete doomed;
        return x;
    }

    string top() {
        return head->data;
    }

    bool contains(string x) {
        for (StrNode* cur = head; cur != nullptr; cur = cur->next)
            if (cur->data == x)
                return true;
        return false;
    }
};

bool isValidBrackets(string s) {
    CharStack st;
    for (char c : s) {
        if (c == '(' || c == '{' || c == '[')
            st.push(c);
        else if (c == ')' || c == '}' || c == ']') {
            if (st.isEmpty())
                return false;
            char open = st.pop();
            if ((c == ')' && open != '(') || (c == '}' && open != '{') || (c == ']' && open != '['))
                return false;
        }
    }
    return st.isEmpty();
}

const int MAX_ERRORS = 50;

void addError(string errors[], int& count, string msg) {
    if (count < MAX_ERRORS)
        errors[count++] = msg;
}

bool validate_markup(string s, string errors[], int& count) {
    StrStack tags;
    count = 0;
    int i = 0;

    while (i < (int)s.size()) {
        if (s[i] != '<') {
            i++;
            continue;
        }

        size_t close = s.find('>', i);
        if (close == string::npos) {
            addError(errors, count, "Tag at position " + to_string(i) + " is never closed with '>'");
            break;
        }

        string inside = s.substr(i + 1, close - i - 1);
        int pos = i;
        i = close + 1;

        bool closing = false;
        bool selfClosing = false;
        if (!inside.empty() && inside[0] == '/') {
            closing = true;
            inside = inside.substr(1);
        }
        if (!inside.empty() && inside.back() == '/') {
            selfClosing = true;
            inside.pop_back();
        }

        string name;
        for (char c : inside) {
            if (c == ' ')
                break;
            name += c;
        }

        if (name.empty()) {
            addError(errors, count, "Empty tag at position " + to_string(pos));
            continue;
        }
        if (selfClosing && !closing)
            continue;

        if (!closing)
            tags.push(name);
        else if (!tags.isEmpty() && tags.top() == name)
            tags.pop();
        else if (tags.contains(name)) {
            while (tags.top() != name)
                addError(errors, count, "<" + tags.pop() + "> not closed before </" + name + "> at position " + to_string(pos));
            tags.pop();
        }
        else
            addError(errors, count, "Unexpected </" + name + "> at position " + to_string(pos));
    }

    while (!tags.isEmpty())
        addError(errors, count, "<" + tags.pop() + "> is never closed");

    return count == 0;
}

void showMenu() {
    cout << endl;
    cout << "1.Check Brackets  2.Validate Markup  3.Exit" << endl;
    cout << "Enter choice: ";
}

int main() {
    int choice, count;
    string s;
    string errors[MAX_ERRORS];
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

        switch (choice) {
            case 1:
                cout << "Enter expression: ";
                cin.ignore(1000, '\n');
                getline(cin, s);
                if (isValidBrackets(s))
                    cout << "Balanced" << endl;
                else
                    cout << "Not balanced" << endl;
                break;

            case 2:
                cout << "Enter markup: ";
                cin.ignore(1000, '\n');
                getline(cin, s);
                if (validate_markup(s, errors, count))
                    cout << "Valid markup" << endl;
                else {
                    cout << "Invalid markup, " << count << " error(s):" << endl;
                    for (int i = 0; i < count; i++)
                        cout << "  " << errors[i] << endl;
                }
                break;

            case 3:
                running = false;
                break;

            default:
                cout << "Invalid choice" << endl;
        }
    }

    cout << "Exiting" << endl;
}
