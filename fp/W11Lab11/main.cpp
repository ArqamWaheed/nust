#include <iostream>
using namespace std;

int main() {
    double A[3][3];
    double B[3][3];
    double C[3][3];

    cout << "Enter 9 elements of first 3x3 matrix (row-wise):" << endl;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            cin >> A[i][j];
        }
    }

    cout << "Enter 9 elements of second 3x3 matrix (row-wise):" << endl;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            cin >> B[i][j];
        }
    }

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            C[i][j] = 0;
            for (int k = 0; k < 3; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    cout << "First matrix:" << endl;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) cout << A[i][j] << " ";
        cout << endl;
    }

    cout << "Second matrix:" << endl;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) cout << B[i][j] << " ";
        cout << endl;
    }

    cout << "Product matrix (A * B):" << endl;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) cout << C[i][j] << " ";
        cout << endl;
    }

    return 0;
}
