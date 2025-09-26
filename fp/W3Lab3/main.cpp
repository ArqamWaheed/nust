#include <iostream>
using namespace std;

int main() {
    float num1;
    float num2;

    cout << "Enter the number you want to increment: ";
    cin >> num1;
    cout << "Enter the number you want to decrement: ";
    cin >> num2; 

    cout << "\nNumber 1: " << ++num1 << endl;
    cout << "Number 2: " << --num2 << endl;
    return 0;
}   