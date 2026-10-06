#include <iostream>
#include <string>
using namespace std;

struct Coach {
    int number;
    string type;
    int capacity;
    int passengers;
    Coach* prev;
    Coach* next;

    Coach(int n, string t, int c, int p) {
        number = n;
        type = t;
        capacity = c;
        passengers = p;
        prev = nullptr;
        next = nullptr;
    }
};

Coach* head = nullptr;
Coach* current = nullptr;

void printCoach(Coach* c) {
    cout << "Coach " << c->number << " (" << c->type << ") " << c->passengers << "/"
        << c->capacity << " passengers, " << c->capacity - c->passengers << " seats free" << endl;
}

Coach* findCoach(int number) {
    if (head == nullptr)
        return nullptr;
    Coach* cur = head;
    do {
        if (cur->number == number)
            return cur;
        cur = cur->next;
    } while (cur != head);
    return nullptr;
}

bool insertAfter(Coach* pos, int number, string type, int capacity, int passengers) {
    if (findCoach(number) != nullptr) {
        cout << "Coach " << number << " already exists" << endl;
        return false;
    }

    Coach* fresh = new Coach(number, type, capacity, passengers);

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
    printCoach(fresh);
    return true;
}

bool addCoach(int number, string type, int capacity, int passengers) {
    return insertAfter(head == nullptr ? nullptr : head->prev, number, type, capacity, passengers);
}

void insertCoach(int after, int number, string type, int capacity, int passengers) {
    Coach* pos = findCoach(after);
    if (pos == nullptr) {
        cout << "Coach " << after << " not found" << endl;
        return;
    }
    insertAfter(pos, number, type, capacity, passengers);
}

void removeCoach(int number) {
    Coach* doomed = findCoach(number);
    if (doomed == nullptr) {
        cout << "Coach " << number << " not found" << endl;
        return;
    }

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
    printCoach(doomed);
    delete doomed;
}

void displayCurrent() {
    if (current == nullptr) {
        cout << "Train is empty" << endl;
        return;
    }
    cout << "Current coach: ";
    printCoach(current);
}

void moveForward() {
    if (current == nullptr) {
        cout << "Train is empty" << endl;
        return;
    }
    current = current->next;
    displayCurrent();
}

void moveBackward() {
    if (current == nullptr) {
        cout << "Train is empty" << endl;
        return;
    }
    current = current->prev;
    displayCurrent();
}

void displayClockwise() {
    if (head == nullptr) {
        cout << "Train is empty" << endl;
        return;
    }
    cout << "Train (clockwise):" << endl;
    Coach* cur = head;
    do {
        cout << "  ";
        printCoach(cur);
        cur = cur->next;
    } while (cur != head);
}

void displayAntiClockwise() {
    if (head == nullptr) {
        cout << "Train is empty" << endl;
        return;
    }
    cout << "Train (anti-clockwise):" << endl;
    Coach* start = head->prev;
    Coach* cur = start;
    do {
        cout << "  ";
        printCoach(cur);
        cur = cur->prev;
    } while (cur != start);
}

void searchCoach(int number) {
    Coach* found = findCoach(number);
    if (found == nullptr) {
        cout << "Coach " << number << " not found" << endl;
        return;
    }
    cout << "Found: ";
    printCoach(found);
}

void maxAvailable() {
    if (head == nullptr) {
        cout << "Train is empty" << endl;
        return;
    }
    Coach* best = head;
    Coach* cur = head->next;
    while (cur != head) {
        if (cur->capacity - cur->passengers > best->capacity - best->passengers)
            best = cur;
        cur = cur->next;
    }
    cout << "Most seats free: ";
    printCoach(best);
}

// swaps next and prev in every coach, the old last coach becomes the new head
void reverseTrain() {
    if (head == nullptr) {
        cout << "Train is empty" << endl;
        return;
    }
    Coach* cur = head;
    do {
        Coach* temp = cur->next;
        cur->next = cur->prev;
        cur->prev = temp;
        cur = temp;
    } while (cur != head);
    head = head->next;
    cout << "Train reversed" << endl;
}

void clearTrain() {
    if (head == nullptr)
        return;
    head->prev->next = nullptr;
    while (head != nullptr) {
        Coach* doomed = head;
        head = head->next;
        delete doomed;
    }
    current = nullptr;
}

bool readCoach(int &number, string &type, int &capacity, int &passengers) {
    cout << "Enter coach number: ";
    cin >> number;
    cout << "Enter coach type: ";
    cin.ignore(1000, '\n');
    getline(cin, type);
    cout << "Enter passenger capacity: ";
    cin >> capacity;
    cout << "Enter current passengers: ";
    cin >> passengers;
    if (!cin || capacity <= 0 || passengers < 0 || passengers > capacity) {
        cin.clear();
        cin.ignore(1000, '\n');
        cout << "Invalid coach details" << endl;
        return false;
    }
    return true;
}

void showMenu() {
    cout << endl;
    cout << "1.Add  2.Insert after  3.Remove  4.Forward  5.Backward  6.Clockwise" << endl;
    cout << "7.Anti-clockwise  8.Search  9.Max free seats  10.Current  11.Reverse  12.Exit" << endl;
    cout << "Enter choice: ";
}

int main() {
    int n, choice, number, after, capacity, passengers;
    string type;
    bool running = true;

    cout << "Enter number of coaches: ";
    cin >> n;
    while (!cin || n < 0) {
        cin.clear();
        cin.ignore(1000, '\n');
        cout << "Number of coaches can't be negative, enter again: ";
        cin >> n;
    }

    for (int i = 1; i <= n; i++) {
        cout << endl << "Coach " << i << endl;
        if (!readCoach(number, type, capacity, passengers))
            i--;
        else if (!addCoach(number, type, capacity, passengers))
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
                if (readCoach(number, type, capacity, passengers))
                    addCoach(number, type, capacity, passengers);
                break;

            case 2:
                cout << "Insert after coach number: ";
                cin >> after;
                if (findCoach(after) == nullptr) {
                    cout << "Coach " << after << " not found" << endl;
                    break;
                }
                if (readCoach(number, type, capacity, passengers))
                    insertCoach(after, number, type, capacity, passengers);
                break;

            case 3:
                cout << "Enter coach number to remove: ";
                cin >> number;
                removeCoach(number);
                break;

            case 4:
                moveForward();
                break;

            case 5:
                moveBackward();
                break;

            case 6:
                displayClockwise();
                break;

            case 7:
                displayAntiClockwise();
                break;

            case 8:
                cout << "Enter coach number to search: ";
                cin >> number;
                searchCoach(number);
                break;

            case 9:
                maxAvailable();
                break;

            case 10:
                displayCurrent();
                break;

            case 11:
                reverseTrain();
                displayClockwise();
                break;

            case 12:
                running = false;
                break;

            default:
                cout << "Invalid choice" << endl;
        }
    }

    clearTrain();
    cout << "Exiting" << endl;
}
