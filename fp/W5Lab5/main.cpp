#include <iostream>
using namespace std;

int main() {
    int guess;
    int secretNumber = 7;
    do {
        cout << "Guess the number: ";
        cin >> guess;

        if(guess != secretNumber) {
            cout << "Wrong! Try again.\n";
        }

    } while(guess != secretNumber);

    cout << "Correct!";

    return 0;
}
