#include <iostream>
using namespace std;

int main() {
    int number, reversed = 0, remainder;

    cout << "Enter a number: ";
    cin >> number;

    while(number != 0) {
        remainder = number % 10;
        reversed = reversed * 10 + remainder;
        number = number / 10;
    }

    cout << "Reversed number: " << reversed;

    return 0;
}
