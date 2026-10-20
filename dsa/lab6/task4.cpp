#include <iostream>
using namespace std;

const int CAPACITY = 5;

class WaitingRoom {
    int ids[CAPACITY];
    int head;
    int count;
    int nextId;

public:
    WaitingRoom() {
        head = 0;
        count = 0;
        nextId = 1;
    }

    void RegisterPatient() {
        if (count == CAPACITY) {
            cout << "Waiting room is full" << endl;
            return;
        }
        ids[(head + count) % CAPACITY] = nextId;
        count++;
        cout << "Registered patient " << nextId++ << endl;
    }

    void ServePatient() {
        if (count == 0) {
            cout << "No patients waiting" << endl;
            return;
        }
        cout << "Serving patient " << ids[head] << endl;
        head = (head + 1) % CAPACITY;
        count--;
    }

    void CancelAll() {
        head = 0;
        count = 0;
        cout << "All appointments cancelled" << endl;
    }

    bool CanDoctorGoHome() {
        return count == 0;
    }

    void ShowAllPatient() {
        if (count == 0) {
            cout << "No patients waiting" << endl;
            return;
        }
        int sorted[CAPACITY];
        for (int i = 0; i < count; i++)
            sorted[i] = ids[(head + i) % CAPACITY];

        for (int i = 1; i < count; i++) {
            int key = sorted[i];
            int j = i - 1;
            while (j >= 0 && sorted[j] > key) {
                sorted[j + 1] = sorted[j];
                j--;
            }
            sorted[j + 1] = key;
        }

        cout << "Waiting patients:";
        for (int i = 0; i < count; i++)
            cout << " " << sorted[i];
        cout << endl;
    }
};

void showMenu() {
    cout << endl;
    cout << "1.Register  2.Serve  3.Cancel All  4.Can Doctor Go Home" << endl;
    cout << "5.Show All  6.Exit" << endl;
    cout << "Enter choice: ";
}

int main() {
    WaitingRoom room;
    int choice;
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
                room.RegisterPatient();
                break;

            case 2:
                room.ServePatient();
                break;

            case 3:
                room.CancelAll();
                break;

            case 4:
                if (room.CanDoctorGoHome())
                    cout << "Yes, no one is waiting" << endl;
                else
                    cout << "No, patients are still waiting" << endl;
                break;

            case 5:
                room.ShowAllPatient();
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
