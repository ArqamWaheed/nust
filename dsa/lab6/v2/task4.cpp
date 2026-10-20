#include <iostream>
#include <string>
using namespace std;

const int ROOM_SIZE = 6;

struct Patient {
    int id;
    string name;
};

class WaitingRoom {
    Patient seats[ROOM_SIZE];
    int frontIdx;
    int rearIdx;
    int waiting;
    int lastId;

public:
    WaitingRoom() {
        frontIdx = 0;
        rearIdx = -1;
        waiting = 0;
        lastId = 0;
    }

    bool isFull() { return waiting == ROOM_SIZE; }

    void RegisterPatient(string name) {
        if (isFull()) {
            cout << "  Sorry " << name << ", the waiting room is full" << endl;
            return;
        }
        lastId++;
        rearIdx = (rearIdx + 1) % ROOM_SIZE;
        seats[rearIdx].id = lastId;
        seats[rearIdx].name = name;
        waiting++;
        cout << "  " << name << " registered with ID " << lastId << endl;
    }

    void ServePatient() {
        if (waiting == 0) {
            cout << "  Nobody to serve" << endl;
            return;
        }
        Patient p = seats[frontIdx];
        frontIdx = (frontIdx + 1) % ROOM_SIZE;
        waiting--;
        cout << "  Doctor is now seeing patient " << p.id << " (" << p.name << ")" << endl;
    }

    void CancelAll() {
        cout << "  Cancelled " << waiting << " appointment(s), doctor is off to lunch" << endl;
        frontIdx = 0;
        rearIdx = -1;
        waiting = 0;
    }

    bool CanDoctorGoHome() {
        return waiting == 0;
    }

    void ShowAllPatient() {
        if (waiting == 0) {
            cout << "  Waiting room is empty" << endl;
            return;
        }

        Patient list[ROOM_SIZE];
        for (int i = 0; i < waiting; i++)
            list[i] = seats[(frontIdx + i) % ROOM_SIZE];

        for (int i = 0; i < waiting - 1; i++) {
            int smallest = i;
            for (int j = i + 1; j < waiting; j++)
                if (list[j].id < list[smallest].id)
                    smallest = j;
            Patient tmp = list[i];
            list[i] = list[smallest];
            list[smallest] = tmp;
        }

        cout << "  " << waiting << " waiting (sorted by ID):" << endl;
        for (int i = 0; i < waiting; i++)
            cout << "    " << list[i].id << "  " << list[i].name << endl;
    }
};

int main() {
    WaitingRoom room;
    int choice = -1;
    string name;

    while (choice != 0) {
        cout << "\n[1] Register  [2] Serve  [3] Cancel all  [4] Can doctor go home  [5] Show all  [0] Exit" << endl;
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

        switch (choice) {
            case 1:
                cout << "Patient name: ";
                cin.ignore(1000, '\n');
                getline(cin, name);
                room.RegisterPatient(name);
                break;
            case 2:
                room.ServePatient();
                break;
            case 3:
                room.CancelAll();
                break;
            case 4:
                cout << (room.CanDoctorGoHome() ? "  true, nobody is waiting" : "  false, patients are still waiting") << endl;
                break;
            case 5:
                room.ShowAllPatient();
                break;
            case 0:
                break;
            default:
                cout << "Please choose 0-5" << endl;
        }
    }

    cout << "Goodbye" << endl;
}
