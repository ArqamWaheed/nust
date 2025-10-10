#include <iostream>
using namespace std;

int main() {
    int number, temp, remainder, sum = 0;

    cout << "Enter a number: ";
    cin >> number;
    temp = number;
    while(temp != 0) {
        remainder = temp % 10;
        sum = sum + (remainder * remainder * remainder);
        temp = temp / 10;
    }
    if(sum == number)
        cout << "Armstrong number";
    else
        cout << "Not an Armstrong number";

    return 0;
}
