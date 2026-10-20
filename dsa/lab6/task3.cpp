#include <iostream>
#include <string>
using namespace std;

struct PrintRequest {
    int id;
    int arrival;
    int processing;
};

class CircularQueue {
    PrintRequest* data;
    int capacity;
    int head;
    int count;

public:
    CircularQueue(int cap) {
        capacity = cap;
        data = new PrintRequest[capacity];
        head = 0;
        count = 0;
    }

    ~CircularQueue() {
        delete[] data;
    }

    bool isEmpty() {
        return count == 0;
    }

    bool isFull() {
        return count == capacity;
    }

    int size() {
        return count;
    }

    void resize(int newCapacity) {
        cout << "Resizing from " << capacity << " to " << newCapacity << endl;
        PrintRequest* fresh = new PrintRequest[newCapacity];
        for (int i = 0; i < count; i++)
            fresh[i] = data[(head + i) % capacity];
        delete[] data;
        data = fresh;
        capacity = newCapacity;
        head = 0;
    }

    void enqueue(PrintRequest x) {
        if (isFull())
            resize(capacity * 2);
        data[(head + count) % capacity] = x;
        count++;
    }

    PrintRequest dequeue() {
        PrintRequest x = data[head];
        head = (head + 1) % capacity;
        count--;
        if (capacity > 4 && count <= capacity / 4)
            resize(capacity / 2);
        return x;
    }

    PrintRequest front() {
        return data[head];
    }

    void display() {
        cout << "Capacity: " << capacity << "  Size: " << count;
        if (count > 0)
            cout << "  Front index: " << head << "  Rear index: " << (head + count - 1) % capacity;
        cout << endl;
        for (int i = 0; i < capacity; i++) {
            int offset = (i - head + capacity) % capacity;
            cout << "  [" << i << "] ";
            if (offset < count)
                cout << "Req " << data[i].id << " (arrival " << data[i].arrival << ", time " << data[i].processing << ")";
            else
                cout << "empty";
            cout << endl;
        }
    }
};

void showMenu() {
    cout << endl;
    cout << "1.Add Request  2.Process Request  3.Front  4.Show Queue" << endl;
    cout << "5.Average Waiting Time  6.Exit" << endl;
    cout << "Enter choice: ";
}

int main() {
    CircularQueue queue(4);
    int choice, arrival, processing;
    int nextId = 1;
    int lastArrival = 0;
    int clock = 0;
    int totalWait = 0;
    int processed = 0;
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
                cout << "Enter arrival time: ";
                cin >> arrival;
                cout << "Enter processing time: ";
                cin >> processing;
                if (arrival < lastArrival || processing <= 0) {
                    cout << "Arrival must be at least " << lastArrival << " and processing time must be positive" << endl;
                    break;
                }
                lastArrival = arrival;
                queue.enqueue({nextId, arrival, processing});
                cout << "Added request " << nextId++ << endl;
                queue.display();
                break;

            case 2: {
                if (queue.isEmpty()) {
                    cout << "No requests waiting" << endl;
                    break;
                }
                PrintRequest r = queue.dequeue();
                int start = clock > r.arrival ? clock : r.arrival;
                int wait = start - r.arrival;
                clock = start + r.processing;
                totalWait += wait;
                processed++;
                cout << "Printed request " << r.id << ": started at " << start << ", finished at " << clock << ", waited " << wait << endl;
                queue.display();
                break;
            }

            case 3:
                if (queue.isEmpty())
                    cout << "No requests waiting" << endl;
                else {
                    PrintRequest r = queue.front();
                    cout << "Next: Req " << r.id << " (arrival " << r.arrival << ", time " << r.processing << ")" << endl;
                }
                break;

            case 4:
                queue.display();
                break;

            case 5:
                if (processed == 0)
                    cout << "No requests processed yet" << endl;
                else
                    cout << "Processed " << processed << " request(s), average waiting time: " << (double)totalWait / processed << endl;
                break;

            case 6:
                running = false;
                break;

            default:
                cout << "Invalid choice" << endl;
        }
    }

    cout << "Exiting" << endl;
}
