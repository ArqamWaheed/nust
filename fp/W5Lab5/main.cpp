#include <iostream>
using namespace std;

int main() {
    int choice, num1, num2;

    do {
        cout << "1. Add  2. Subtract  3. Multiply  0. Exit";
        cout << "\nEnter your choice: ";
        cin >> choice;
        if(choice == 0) {
            break;
        }
        cout << "Enter two numbers: ";
        cin >> num1 >> num2;
        switch(choice) {
            case 1:
                cout << "Result: " << num1 + num2;
                break;
            case 2:
                cout << "Result: " << num1 - num2;
                break;
            case 3:
                cout << "Result: " << num1 * num2;
                break;
            default:
                cout << "Invalid option!";
        }

        cout << endl;

    } while(choice != 0);

    return 0;
}
