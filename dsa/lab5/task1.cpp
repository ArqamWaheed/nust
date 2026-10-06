#include <iostream>
#include <string>
using namespace std;

struct Tab {
    int id;
    string title;
    string url;
    Tab* prev;
    Tab* next;

    Tab(int i, string t, string u) {
        id = i;
        title = t;
        url = u;
        prev = nullptr;
        next = nullptr;
    }
};

Tab* current = nullptr;

void printTab(Tab* t) {
    cout << "[" << t->id << "] " << t->title << " - " << t->url << endl;
}

Tab* findTab(int id) {
    if (current == nullptr)
        return nullptr;
    Tab* cur = current;
    do {
        if (cur->id == id)
            return cur;
        cur = cur->next;
    } while (cur != current);
    return nullptr;
}

void openTab(int id, string title, string url) {
    if (findTab(id) != nullptr) {
        cout << "A tab with ID " << id << " already exists" << endl;
        return;
    }

    Tab* fresh = new Tab(id, title, url);

    if (current == nullptr) {
        fresh->next = fresh;
        fresh->prev = fresh;
        current = fresh;
    }
    else {
        fresh->next = current->next;
        fresh->prev = current;
        current->next->prev = fresh;
        current->next = fresh;
    }
    cout << "Opened: ";
    printTab(fresh);
}

void closeTab() {
    if (current == nullptr) {
        cout << "No tabs open" << endl;
        return;
    }

    Tab* doomed = current;
    if (doomed->next == doomed)
        current = nullptr;
    else {
        doomed->prev->next = doomed->next;
        doomed->next->prev = doomed->prev;
        current = doomed->next;
    }
    cout << "Closed: ";
    printTab(doomed);
    delete doomed;
}

void displayCurrent() {
    if (current == nullptr) {
        cout << "No tabs open" << endl;
        return;
    }
    cout << "Current tab: ";
    printTab(current);
}

void moveNext() {
    if (current == nullptr) {
        cout << "No tabs open" << endl;
        return;
    }
    current = current->next;
    displayCurrent();
}

void movePrevious() {
    if (current == nullptr) {
        cout << "No tabs open" << endl;
        return;
    }
    current = current->prev;
    displayCurrent();
}

void displayForward() {
    if (current == nullptr) {
        cout << "No tabs open" << endl;
        return;
    }
    cout << "Tabs (forward from current):" << endl;
    Tab* cur = current;
    do {
        cout << "  ";
        printTab(cur);
        cur = cur->next;
    } while (cur != current);
}

void displayBackward() {
    if (current == nullptr) {
        cout << "No tabs open" << endl;
        return;
    }
    cout << "Tabs (backward from current):" << endl;
    Tab* cur = current;
    do {
        cout << "  ";
        printTab(cur);
        cur = cur->prev;
    } while (cur != current);
}

void searchTab(int id) {
    Tab* found = findTab(id);
    if (found == nullptr) {
        cout << "Tab " << id << " not found" << endl;
        return;
    }
    cout << "Found: ";
    printTab(found);
}

void closeAll() {
    while (current != nullptr) {
        Tab* doomed = current;
        if (doomed->next == doomed)
            current = nullptr;
        else {
            doomed->prev->next = doomed->next;
            doomed->next->prev = doomed->prev;
            current = doomed->next;
        }
        delete doomed;
    }
}

void showMenu() {
    cout << endl;
    cout << "1.Open  2.Close  3.Next  4.Previous  5.Current" << endl;
    cout << "6.Forward  7.Backward  8.Search  9.Exit" << endl;
    cout << "Enter choice: ";
}

int main() {
    int choice, id;
    string title, url;
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
                cout << "Enter tab ID: ";
                cin >> id;
                cout << "Enter website title: ";
                cin.ignore(1000, '\n');
                getline(cin, title);
                cout << "Enter URL: ";
                getline(cin, url);
                openTab(id, title, url);
                break;

            case 2:
                closeTab();
                break;

            case 3:
                moveNext();
                break;

            case 4:
                movePrevious();
                break;

            case 5:
                displayCurrent();
                break;

            case 6:
                displayForward();
                break;

            case 7:
                displayBackward();
                break;

            case 8:
                cout << "Enter tab ID to search: ";
                cin >> id;
                searchTab(id);
                break;

            case 9:
                running = false;
                break;

            default:
                cout << "Invalid choice" << endl;
        }
    }

    closeAll();
    cout << "Exiting" << endl;
}
