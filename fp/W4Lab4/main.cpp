#include <iostream>
using namespace std;

int main() {
    cout << "Enter three angles of the triangle (in degrees), separated by spaces: ";

    float a, b, c;
    cin >> a >> b >> c;


    float sum = a + b + c;

    if (sum == 180) {
        cout << "This is a valid triangle";
    } else {
        cout << "This is an invalid triangle";
    }

    return 0;
}