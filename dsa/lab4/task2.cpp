#include <iostream>
using namespace std;

struct Person {
    int id;
    Person* next;

    Person(int value) {
        id = value;
        next = nullptr;
    }
};

// builds 1 -> 2 -> ... -> n and joins the last one back to 1
// returns the LAST node, so its next is person 1 and deleting person 1
// is easy (we always have the node before it)
Person* createCircle(int n) {
    Person* first = new Person(1);
    Person* last = first;

    for (int i = 2; i <= n; i++) {
        last->next = new Person(i);
        last = last->next;
    }
    last->next = first;     // no NULL at the end, it's a circle
    return last;
}

void displayCircle(Person* last) {
    Person* cur = last->next;
    int shown = 0;
    do {
        cout << cur->id << " -> ";
        cur = cur->next;
        shown++;
        if (shown % 15 == 0 && cur != last->next)
            cout << endl << "        ";     // wrap long circles so they stay readable
    } while (cur != last->next);
    cout << "(back to " << last->next->id << ")" << endl;
}

// behind always sits one node before the person being counted
// move it k-1 times, then the node after it is the k-th person
int josephus(Person* last, int n, int k) {
    Person* behind = last;
    int alive = n;

    int removed = 0;
    cout << "Eliminated order: ";
    while (alive > 1) {
        for (int count = 1; count < k; count++)
            behind = behind->next;

        Person* doomed = behind->next;
        cout << doomed->id << " ";
        removed++;
        if (removed % 20 == 0 && alive > 2)
            cout << endl << "                  ";

        behind->next = doomed->next;    // skip over the eliminated person
        delete doomed;
        alive--;
        // counting restarts from behind->next, the person after the one removed
    }
    cout << endl;

    int survivor = behind->id;
    delete behind;      // last node left, points to itself
    return survivor;
}

int main() {
    int n, k;

    cout << "Enter number of people (N): ";
    cin >> n;
    while (!cin || n < 1) {
        cin.clear();
        cin.ignore(1000, '\n');
        cout << "N must be at least 1, enter again: ";
        cin >> n;
    }

    cout << "Enter step count (k): ";
    cin >> k;
    while (!cin || k < 1) {
        cin.clear();
        cin.ignore(1000, '\n');
        cout << "k must be at least 1, enter again: ";
        cin >> k;
    }

    Person* last = createCircle(n);
    cout << "Circle: ";
    displayCircle(last);

    int survivor = josephus(last, n, k);
    cout << "Survivor: Person " << survivor << endl;
}
