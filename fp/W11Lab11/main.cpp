#include <iostream>
using namespace std;

int main() {
    double a[3][3];

    cout << "Enter 9 elements of 3x3 matrix (row-wise):" << endl;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            cin >> a[i][j];
        }
    }

    cout << "Original matrix:" << endl;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            cout << a[i][j] << " ";
        }
        cout << endl;
    }

    double det = a[0][0] * (a[1][1]*a[2][2] - a[1][2]*a[2][1])
               - a[0][1] * (a[1][0]*a[2][2] - a[1][2]*a[2][0])
               + a[0][2] * (a[1][0]*a[2][1] - a[1][1]*a[2][0]);

    double c[3][3];
    c[0][0] =  (a[1][1]*a[2][2] - a[1][2]*a[2][1]);
    c[0][1] = -(a[1][0]*a[2][2] - a[1][2]*a[2][0]);
    c[0][2] =  (a[1][0]*a[2][1] - a[1][1]*a[2][0]);

    c[1][0] = -(a[0][1]*a[2][2] - a[0][2]*a[2][1]);
    c[1][1] =  (a[0][0]*a[2][2] - a[0][2]*a[2][0]);
    c[1][2] = -(a[0][0]*a[2][1] - a[0][1]*a[2][0]);

    c[2][0] =  (a[0][1]*a[1][2] - a[0][2]*a[1][1]);
    c[2][1] = -(a[0][0]*a[1][2] - a[0][2]*a[1][0]);
    c[2][2] =  (a[0][0]*a[1][1] - a[0][1]*a[1][0]);

    double inv[3][3];
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            inv[i][j] = c[j][i] / det; 
        }
    }

    cout << "Inverse matrix:" << endl;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            cout << inv[i][j] << " ";
        }
        cout << endl;
    }

    return 0;
}
