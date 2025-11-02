#include <iostream>
using namespace std;

inline int square(int x) {
    return x * x;
}

inline int cube(int x) {
    return x * x * x;
}

int main() {
    int num;
    cout << "Enter a number: ";
    cin >> num;
    cout << "Square of the number = " << square(num) << endl;
    cout << "Cube of the number = " << cube(num) << endl;
    return 0;
}