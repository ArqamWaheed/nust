#include <iostream>
#include <string>
using namespace std;

class StringPool {
    string *stringPool;
    int currentSize;
    int maxSize;

public:
    StringPool() {
        maxSize = 5;
        currentSize = 0;
        stringPool = new string[maxSize];
    }

    void addString(const string &value) {
        if (currentSize == maxSize) {
            cout << "Pool is full, \"" << value << "\" was not added." << endl;
            return;
        }
        stringPool[currentSize] = value;
        currentSize++;
        cout << "Added   : " << value << endl;
    }

    void removeString(const string &value) {
        for (int i = 0; i < currentSize; i++) {
            if (stringPool[i] == value) {
                for (int j = i; j < currentSize - 1; j++)
                    stringPool[j] = stringPool[j + 1];
                currentSize--;
                cout << "Removed : " << value << endl;
                return;
            }
        }
        cout << "Not found: " << value << endl;
    }

    void showPool() const {
        cout << "Pool (" << currentSize << "/" << maxSize << "): ";
        for (int i = 0; i < currentSize; i++)
            cout << "[" << stringPool[i] << "] ";
        cout << endl;
    }
};

int main() {
    StringPool pool;

    pool.addString("first string in the pool");
    pool.addString("second string in the pool");
    pool.addString("third string in the pool");
    pool.addString("fourth string in the pool");
    pool.showPool();

    pool.removeString("second string in the pool");
    pool.removeString("fourth string in the pool");
    pool.showPool();

    return 0;
}
