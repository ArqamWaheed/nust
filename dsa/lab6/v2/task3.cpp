#include <iostream>
#include <iomanip>
using namespace std;

struct Job {
    int id;
    int arrival;
    int duration;
};

class PrintQueue {
    Job* buffer;
    int capacity;
    int frontIdx;
    int rearIdx;
    int count;

public:
    PrintQueue() {
        capacity = 2;
        buffer = new Job[capacity];
        frontIdx = 0;
        rearIdx = -1;
        count = 0;
    }

    ~PrintQueue() { delete[] buffer; }

    bool isEmpty() { return count == 0; }
    bool isFull() { return count == capacity; }

    void resize(int newCapacity) {
        Job* bigger = new Job[newCapacity];
        int idx = frontIdx;
        for (int i = 0; i < count; i++) {
            bigger[i] = buffer[idx];
            idx = (idx + 1) % capacity;
        }
        cout << "        [resize " << capacity << " -> " << newCapacity << "]" << endl;
        delete[] buffer;
        buffer = bigger;
        capacity = newCapacity;
        frontIdx = 0;
        rearIdx = count - 1;
    }

    void enqueue(Job j) {
        if (isFull())
            resize(capacity * 2);
        rearIdx = (rearIdx + 1) % capacity;
        buffer[rearIdx] = j;
        count++;
    }

    Job dequeue() {
        Job j = buffer[frontIdx];
        frontIdx = (frontIdx + 1) % capacity;
        count--;
        if (capacity > 2 && count < capacity / 4)
            resize(capacity / 2);
        return j;
    }

    Job front() { return buffer[frontIdx]; }

    void print() {
        cout << "        queue (cap " << capacity << "): ";
        if (isEmpty()) {
            cout << "<empty>" << endl;
            return;
        }
        int idx = frontIdx;
        for (int i = 0; i < count; i++) {
            cout << "J" << buffer[idx].id << " ";
            idx = (idx + 1) % capacity;
        }
        cout << "  front=" << frontIdx << " rear=" << rearIdx << endl;
    }
};

void simulate(Job jobs[], int n) {
    PrintQueue q;
    int next = 0;
    int done = 0;
    int busyUntil = 0;
    int printing = -1;
    int totalWait = 0;
    int clock = 0;

    cout << "\n--- Simulation ---" << endl;
    while (done < n) {
        if (printing != -1 && clock == busyUntil) {
            cout << "t=" << setw(2) << clock << "  J" << printing << " finished" << endl;
            printing = -1;
            done++;
            if (done == n)
                break;
        }

        while (next < n && jobs[next].arrival == clock) {
            cout << "t=" << setw(2) << clock << "  J" << jobs[next].id << " arrives (needs " << jobs[next].duration << ")" << endl;
            q.enqueue(jobs[next]);
            q.print();
            next++;
        }

        if (printing == -1 && !q.isEmpty()) {
            Job j = q.front();
            int wait = clock - j.arrival;
            totalWait += wait;
            printing = j.id;
            busyUntil = clock + j.duration;
            cout << "t=" << setw(2) << clock << "  J" << j.id << " starts printing, waited " << wait << endl;
            q.dequeue();
            q.print();
        }

        clock++;
    }

    cout << "\nAll " << n << " jobs printed by t=" << clock << endl;
    cout << "Average waiting time = " << totalWait << " / " << n << " = " << fixed << setprecision(2) << (double)totalWait / n << endl;
    cout.unsetf(ios::fixed);
}

int main() {
    char again = 'y';

    while (again == 'y' || again == 'Y') {
        int n;
        cout << "Number of print requests: ";
        if (!(cin >> n) || n <= 0) {
            cout << "Invalid number" << endl;
            return 0;
        }

        Job* jobs = new Job[n];
        cout << "Enter ID, arrival time and processing time for each request (arrival in increasing order)" << endl;
        for (int i = 0; i < n; i++) {
            cout << "Request " << i + 1 << ": ";
            if (!(cin >> jobs[i].id >> jobs[i].arrival >> jobs[i].duration)) {
                cout << "Invalid input" << endl;
                delete[] jobs;
                return 0;
            }
            bool badOrder = i > 0 && jobs[i].arrival < jobs[i - 1].arrival;
            if (jobs[i].arrival < 0 || jobs[i].duration <= 0 || badOrder) {
                cout << "  invalid request, try again" << endl;
                i--;
            }
        }

        simulate(jobs, n);
        delete[] jobs;

        cout << "\nRun another simulation? (y/n): ";
        cin >> again;
    }

    cout << "Goodbye" << endl;
}
