#include <iostream>
#include <string>
#include <iomanip>
using namespace std;

struct Song {
    int id;
    string name;
    int minutes;
    int seconds;
    Song* prev;
    Song* next;

    Song(int i, string n, int m, int s) {
        id = i;
        name = n;
        minutes = m;
        seconds = s;
        prev = nullptr;
        next = nullptr;
    }
};

Song* head = nullptr;
Song* tail = nullptr;
Song* current = nullptr;   // the song the "player" is on right now

void printSong(Song* s) {
    cout << "[" << s->id << "] " << s->name << " (" << s->minutes << ":"
        << setw(2) << setfill('0') << s->seconds << setfill(' ') << ")" << endl;
}

Song* findSong(int id) {
    for (Song* cur = head; cur != nullptr; cur = cur->next)
        if (cur->id == id)
            return cur;
    return nullptr;
}

// new song goes after the tail, tail keeps it O(1)
void addSong(int id, string name, int m, int s) {
    if (findSong(id) != nullptr) {
        cout << "A song with ID " << id << " already exists" << endl;
        return;
    }

    Song* fresh = new Song(id, name, m, s);

    if (head == nullptr) {
        head = tail = current = fresh;
    }
    else {
        tail->next = fresh;
        fresh->prev = tail;
        tail = fresh;
    }
    cout << "Added: ";
    printSong(fresh);
}

// unlinks the node from both sides, head/tail fixed if it was at an end
void deleteSong(int id) {
    Song* doomed = findSong(id);
    if (doomed == nullptr) {
        cout << "Song " << id << " not found" << endl;
        return;
    }

    if (doomed->prev != nullptr)
        doomed->prev->next = doomed->next;
    else
        head = doomed->next;

    if (doomed->next != nullptr)
        doomed->next->prev = doomed->prev;
    else
        tail = doomed->prev;

    // if the player was on this song move it to a neighbour
    if (current == doomed)
        current = (doomed->next != nullptr) ? doomed->next : doomed->prev;

    cout << "Deleted: ";
    printSong(doomed);
    delete doomed;
}

void displayForward() {
    if (head == nullptr) {
        cout << "Playlist is empty" << endl;
        return;
    }
    cout << "Playlist (first to last):" << endl;
    for (Song* cur = head; cur != nullptr; cur = cur->next) {
        cout << "  ";
        printSong(cur);
    }
}

// starts at the tail and follows prev pointers
void displayBackward() {
    if (tail == nullptr) {
        cout << "Playlist is empty" << endl;
        return;
    }
    cout << "Playlist (last to first):" << endl;
    for (Song* cur = tail; cur != nullptr; cur = cur->prev) {
        cout << "  ";
        printSong(cur);
    }
}

void searchSong(int id) {
    Song* found = findSong(id);
    if (found == nullptr) {
        cout << "Song " << id << " not found" << endl;
        return;
    }
    cout << "Found: ";
    printSong(found);
}

void playCurrent() {
    if (current == nullptr) {
        cout << "Playlist is empty" << endl;
        return;
    }
    cout << "Now playing: ";
    printSong(current);
}

void playNext() {
    if (current == nullptr) {
        cout << "Playlist is empty" << endl;
        return;
    }
    if (current->next == nullptr) {
        cout << "Already at the last song" << endl;
        return;
    }
    current = current->next;
    playCurrent();
}

void playPrevious() {
    if (current == nullptr) {
        cout << "Playlist is empty" << endl;
        return;
    }
    if (current->prev == nullptr) {
        cout << "Already at the first song" << endl;
        return;
    }
    current = current->prev;
    playCurrent();
}

// swaps prev and next in every node, then swaps head and tail
// no new nodes, no data copied, only the pointers change
void reversePlaylist() {
    Song* cur = head;
    while (cur != nullptr) {
        Song* temp = cur->next;
        cur->next = cur->prev;
        cur->prev = temp;
        cur = temp;     // old next, since the pointers are swapped now
    }
    Song* temp = head;
    head = tail;
    tail = temp;
    cout << "Playlist reversed" << endl;
}

void clearPlaylist() {
    while (head != nullptr) {
        Song* doomed = head;
        head = head->next;
        delete doomed;
    }
    tail = current = nullptr;
}

// reads a duration like 3:45 and checks it
bool readDuration(int &m, int &s) {
    char colon;
    cin >> m >> colon >> s;
    if (!cin || colon != ':' || m < 0 || s < 0 || s > 59) {
        cin.clear();
        cin.ignore(1000, '\n');
        return false;
    }
    return true;
}

void showMenu() {
    cout << endl;
    cout << "1.Add  2.Delete  3.Forward  4.Backward  5.Search  6.Next  7.Previous  8.Reverse  9.Exit" << endl;
    cout << "Enter choice: ";
}

int main() {
    int choice, id, m, s;
    string name;
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
                cout << "Enter song ID: ";
                cin >> id;
                cout << "Enter song name: ";
                cin.ignore(1000, '\n');
                getline(cin, name);
                cout << "Enter duration (mm:ss): ";
                if (!readDuration(m, s)) {
                    cout << "Invalid duration" << endl;
                    break;
                }
                addSong(id, name, m, s);
                break;

            case 2:
                cout << "Enter song ID to delete: ";
                cin >> id;
                deleteSong(id);
                break;

            case 3:
                displayForward();
                break;

            case 4:
                displayBackward();
                break;

            case 5:
                cout << "Enter song ID to search: ";
                cin >> id;
                searchSong(id);
                break;

            case 6:
                playNext();
                break;

            case 7:
                playPrevious();
                break;

            case 8:
                reversePlaylist();
                displayForward();
                break;

            case 9:
                running = false;
                break;

            default:
                cout << "Invalid choice" << endl;
        }
    }

    clearPlaylist();
    cout << "Exiting" << endl;
}
