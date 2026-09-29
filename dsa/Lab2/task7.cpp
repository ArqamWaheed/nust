#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "Enter number of students (1-10): ";
    while (!(cin >> n) || n < 1 || n > 10) {
        cin.clear();
        cin.ignore(1000, '\n');
        cout << "n must be between 1 and 10. Enter again: ";
    }

    int *marks = new int[n];
    cout << "Enter " << n << " marks: ";
    for (int i = 0; i < n; i++)
        cin >> *(marks + i);

    // the old block only has room for n ints, so allocate a bigger one
    int *newBlock = new int[n + 1];
    for (int i = 0; i < n; i++)
        *(newBlock + i) = *(marks + i);

    cout << "Enter mark of the new student: ";
    cin >> *(newBlock + n);     // last position of the new block

    delete[] marks;             // release the old block
    marks = newBlock;           // original pointer now refers to the new block
    newBlock = nullptr;
    n = n + 1;                  // update the stored size

    cout << "All marks: ";
    for (int i = 0; i < n; i++)
        cout << *(marks + i) << " ";
    cout << endl;

    delete[] marks;             // final block released exactly once
    marks = nullptr;

    return 0;
}
