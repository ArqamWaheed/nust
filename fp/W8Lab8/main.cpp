#include <iostream>
using namespace std;

int multiply(int a, int b, int c = 1, int d = 1, int e = 1) {
    return a * b * c * d * e;
}

int main() {
    int n;
    cout << "Enter number of integers to multiply (2-5): ";
    cin >> n;
    int a, b, c = 1, d = 1, e = 1;
    cout << "Enter " << n << " integers: ";
    cin >> a >> b;
    if (n >= 3) cin >> c;
    if (n >= 4) cin >> d;
    if (n == 5) cin >> e;
    int result;
    switch (n) {
        case 2:
            result = multiply(a, b);
            break;
        case 3:
            result = multiply(a, b, c);
            break;
        case 4:
            result = multiply(a, b, c, d);
            break;
        case 5:
            result = multiply(a, b, c, d, e);
            break;
        default:
            cout << "Invalid number of integers." << endl;
            return 1;
    }
    cout << "Product: " << result << endl;
    return 0;
}