#include <iostream>
using namespace std;

// reads a positive integer, asks again if the input is invalid
int readPositive(const char *prompt) {
    int value;
    cout << prompt;
    while (!(cin >> value) || value <= 0) {
        cin.clear();
        cin.ignore(1000, '\n');
        cout << "Invalid, must be greater than 0. " << prompt;
    }
    return value;
}

int main() {
    int rows = readPositive("Enter number of students: ");
    int cols = readPositive("Enter number of subjects: ");

    // array of row pointers, then a separate block of cols ints for each row
    int **marks = new int*[rows];
    for (int r = 0; r < rows; r++)
        *(marks + r) = new int[cols];

    // input loop written completely in pointer notation
    for (int r = 0; r < rows; r++) {
        cout << "Enter " << cols << " marks of student " << r + 1 << ": ";
        for (int c = 0; c < cols; c++)
            cin >> *(*(marks + r) + c);
    }

    // display the matrix
    cout << "\nMarks matrix:" << endl;
    for (int r = 0; r < rows; r++) {
        cout << "Student " << r + 1 << ":";
        for (int c = 0; c < cols; c++)
            cout << "\t" << *(*(marks + r) + c);
        cout << endl;
    }

    // first student's total is the starting best
    int bestTotal = 0;
    int bestStudent = 1;
    for (int c = 0; c < cols; c++)
        bestTotal += marks[0][c];

    cout << "\nTotals: ";
    for (int r = 0; r < rows; r++) {
        int total = 0;
        for (int c = 0; c < cols; c++)
            total += marks[r][c];

        cout << total;
        if (r < rows - 1)
            cout << ", ";

        // strictly greater, so on a tie the first student is kept
        if (total > bestTotal) {
            bestTotal = total;
            bestStudent = r + 1;
        }
    }
    cout << endl;
    cout << "Top student: " << bestStudent << " (total = " << bestTotal << ")" << endl;

    // delete every row first, then the array of row pointers
    for (int r = 0; r < rows; r++)
        delete[] marks[r];
    delete[] marks;
    marks = nullptr;

    return 0;
}
