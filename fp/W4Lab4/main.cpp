#include <iostream>
using namespace std;

int main() {
    int num;

    cout << "Enter a five-digit integer: ";
    cin >> num;

    int d1 = num / 10000;
    int d2 = (num / 1000) % 10;
    int d3 = (num / 100) % 10;
    int d4 = (num / 10) % 10;
    int d5 = num % 10;

    if (d1 == d5 && d2 == d4) {
        cout << "The number is a palindrome." << endl;
    } else {
        cout << "The number is not a palindrome." << endl;
    }
    
    return 0;
}