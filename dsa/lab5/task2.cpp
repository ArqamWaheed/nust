#include <iostream>
#include <string>
using namespace std;

struct Photo {
    int id;
    string name;
    string date;
    string location;
    Photo* prev;
    Photo* next;

    Photo(int i, string n, string d, string l) {
        id = i;
        name = n;
        date = d;
        location = l;
        prev = nullptr;
        next = nullptr;
    }
};

Photo* head = nullptr;
Photo* current = nullptr;

void printPhoto(Photo* p) {
    cout << "[" << p->id << "] " << p->name << ", " << p->date << ", " << p->location << endl;
}

Photo* findPhoto(int id) {
    if (head == nullptr)
        return nullptr;
    Photo* cur = head;
    do {
        if (cur->id == id)
            return cur;
        cur = cur->next;
    } while (cur != head);
    return nullptr;
}

bool insertAfter(Photo* pos, int id, string name, string date, string location) {
    if (findPhoto(id) != nullptr) {
        cout << "A photo with ID " << id << " already exists" << endl;
        return false;
    }

    Photo* fresh = new Photo(id, name, date, location);

    if (head == nullptr) {
        fresh->next = fresh;
        fresh->prev = fresh;
        head = current = fresh;
    }
    else {
        fresh->next = pos->next;
        fresh->prev = pos;
        pos->next->prev = fresh;
        pos->next = fresh;
    }
    cout << "Added: ";
    printPhoto(fresh);
    return true;
}

bool addPhoto(int id, string name, string date, string location) {
    return insertAfter(head == nullptr ? nullptr : head->prev, id, name, date, location);
}

void insertAfterCurrent(int id, string name, string date, string location) {
    insertAfter(current, id, name, date, location);
}

void removeNode(Photo* doomed) {
    if (doomed->next == doomed)
        head = current = nullptr;
    else {
        doomed->prev->next = doomed->next;
        doomed->next->prev = doomed->prev;
        if (head == doomed)
            head = doomed->next;
        if (current == doomed)
            current = doomed->next;
    }
    cout << "Removed: ";
    printPhoto(doomed);
    delete doomed;
}

void removePhoto(int id) {
    Photo* doomed = findPhoto(id);
    if (doomed == nullptr) {
        cout << "Photo " << id << " not found" << endl;
        return;
    }
    removeNode(doomed);
}

void removeCurrent() {
    if (current == nullptr) {
        cout << "Album is empty" << endl;
        return;
    }
    removeNode(current);
}

void displayCurrent() {
    if (current == nullptr) {
        cout << "Album is empty" << endl;
        return;
    }
    cout << "Current photo: ";
    printPhoto(current);
}

void moveNext() {
    if (current == nullptr) {
        cout << "Album is empty" << endl;
        return;
    }
    current = current->next;
    displayCurrent();
}

void movePrevious() {
    if (current == nullptr) {
        cout << "Album is empty" << endl;
        return;
    }
    current = current->prev;
    displayCurrent();
}

void displayForward() {
    if (current == nullptr) {
        cout << "Album is empty" << endl;
        return;
    }
    cout << "Album (forward from current):" << endl;
    Photo* cur = current;
    do {
        cout << "  ";
        printPhoto(cur);
        cur = cur->next;
    } while (cur != current);
}

void displayBackward() {
    if (current == nullptr) {
        cout << "Album is empty" << endl;
        return;
    }
    cout << "Album (backward from current):" << endl;
    Photo* cur = current;
    do {
        cout << "  ";
        printPhoto(cur);
        cur = cur->prev;
    } while (cur != current);
}

void searchPhoto(int id) {
    Photo* found = findPhoto(id);
    if (found == nullptr) {
        cout << "Photo " << id << " not found" << endl;
        return;
    }
    cout << "Found: ";
    printPhoto(found);
}

int countPhotos() {
    if (head == nullptr)
        return 0;
    int count = 0;
    Photo* cur = head;
    do {
        count++;
        cur = cur->next;
    } while (cur != head);
    return count;
}

void clearAlbum() {
    if (head == nullptr)
        return;
    head->prev->next = nullptr;
    while (head != nullptr) {
        Photo* doomed = head;
        head = head->next;
        delete doomed;
    }
    current = nullptr;
}

void readPhoto(int &id, string &name, string &date, string &location) {
    cout << "Enter photo ID: ";
    cin >> id;
    cin.ignore(1000, '\n');
    cout << "Enter photo name: ";
    getline(cin, name);
    cout << "Enter date taken: ";
    getline(cin, date);
    cout << "Enter location: ";
    getline(cin, location);
}

void showMenu() {
    cout << endl;
    cout << "1.Add  2.Insert after current  3.Remove by ID  4.Remove current  5.Next" << endl;
    cout << "6.Previous  7.Forward  8.Backward  9.Search  10.Count  11.Exit" << endl;
    cout << "Enter choice: ";
}

int main() {
    int n, choice, id;
    string name, date, location;
    bool running = true;

    cout << "Enter number of photos: ";
    cin >> n;
    while (!cin || n < 0) {
        cin.clear();
        cin.ignore(1000, '\n');
        cout << "Number of photos can't be negative, enter again: ";
        cin >> n;
    }

    for (int i = 1; i <= n; i++) {
        cout << endl << "Photo " << i << endl;
        readPhoto(id, name, date, location);
        if (!addPhoto(id, name, date, location))
            i--;
    }

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
                readPhoto(id, name, date, location);
                addPhoto(id, name, date, location);
                break;

            case 2:
                readPhoto(id, name, date, location);
                insertAfterCurrent(id, name, date, location);
                break;

            case 3:
                cout << "Enter photo ID to remove: ";
                cin >> id;
                removePhoto(id);
                break;

            case 4:
                removeCurrent();
                break;

            case 5:
                moveNext();
                break;

            case 6:
                movePrevious();
                break;

            case 7:
                displayForward();
                break;

            case 8:
                displayBackward();
                break;

            case 9:
                cout << "Enter photo ID to search: ";
                cin >> id;
                searchPhoto(id);
                break;

            case 10:
                cout << "Total photos: " << countPhotos() << endl;
                break;

            case 11:
                running = false;
                break;

            default:
                cout << "Invalid choice" << endl;
        }
    }

    clearAlbum();
    cout << "Exiting" << endl;
}
