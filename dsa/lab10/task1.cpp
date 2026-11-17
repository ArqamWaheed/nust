#include <iostream>
using namespace std;

// linked list of containers
struct Container {
    int id;
    int weight;
    Container* next;
    Container(int i, int w) {
        id = i;
        weight = w;
        next = nullptr;
    }
};

// queue of trucks (linked), each truck remembers what it carries
struct Truck {
    int number;
    int remaining;
    int loaded[20];
    int count;
    Truck* next;
    Truck(int n, int cap) {
        number = n;
        remaining = cap;
        count = 0;
        next = nullptr;
    }
};

struct TruckQueue {
    Truck* front;
    Truck* back;
    TruckQueue() {
        front = nullptr;
        back = nullptr;
    }
    void enqueue(int number, int cap) {
        Truck* t = new Truck(number, cap);
        if (back == nullptr)
            front = back = t;
        else {
            back->next = t;
            back = t;
        }
    }
};

int steps = 0;
int pruned = 0;

int totalRemaining(Truck* front) {
    int sum = 0;
    for (Truck* t = front; t != nullptr; t = t->next)
        sum += t->remaining;
    return sum;
}

// cur = container being placed, left = total weight of cur and everything after it
bool load(Container* cur, int left, TruckQueue& q) {
    steps++;
    if (cur == nullptr)
        return true;
    // prune: remaining weight can never fit in the remaining capacity
    if (left > totalRemaining(q.front)) {
        pruned++;
        return false;
    }
    for (Truck* t = q.front; t != nullptr; t = t->next) {
        // prune: this truck cannot take the container
        if (t->remaining < cur->weight) {
            pruned++;
            continue;
        }
        t->remaining -= cur->weight;
        t->loaded[t->count++] = cur->id;
        if (load(cur->next, left - cur->weight, q))
            return true;
        t->count--;           // undo
        t->remaining += cur->weight;
    }
    return false;
}

void solve(int ids[], int weights[], int n, int trucks, int cap) {
    Container* head = nullptr;
    Container* tail = nullptr;
    int total = 0;
    for (int i = 0; i < n; i++) {
        Container* c = new Container(ids[i], weights[i]);
        if (head == nullptr)
            head = tail = c;
        else {
            tail->next = c;
            tail = c;
        }
        total += weights[i];
    }
    TruckQueue q;
    for (int i = 1; i <= trucks; i++)
        q.enqueue(i, cap);

    steps = 0;
    pruned = 0;
    cout << n << " containers, total " << total << " tons, " << trucks
         << " trucks of capacity " << cap << endl;
    if (load(head, total, q)) {
        for (Truck* t = q.front; t != nullptr; t = t->next) {
            cout << "Truck " << t->number << ": ";
            int used = 0;
            for (int i = 0; i < t->count; i++) {
                cout << "C" << t->loaded[i] << " ";
                for (Container* c = head; c != nullptr; c = c->next)
                    if (c->id == t->loaded[i])
                        used += c->weight;
            }
            if (t->count == 0)
                cout << "(empty)";
            cout << "-> " << used << "/" << cap << " tons" << endl;
        }
    } else
        cout << "Insufficient truck capacity." << endl;
    cout << "recursive calls: " << steps << ", branches pruned: " << pruned << endl << endl;

    while (head != nullptr) {
        Container* d = head;
        head = head->next;
        delete d;
    }
    while (q.front != nullptr) {
        Truck* d = q.front;
        q.front = q.front->next;
        delete d;
    }
}

int main() {
    int ids1[] = {1, 2, 3, 4, 5, 6};
    int w1[] = {5, 8, 3, 7, 2, 6};
    solve(ids1, w1, 6, 3, 12);

    int ids2[] = {1, 2, 3, 4, 5};
    int w2[] = {9, 8, 7, 6, 5};
    solve(ids2, w2, 5, 2, 15);

    int ids3[] = {1, 2, 3};
    int w3[] = {10, 4, 9};
    solve(ids3, w3, 3, 2, 12);
    return 0;
}
