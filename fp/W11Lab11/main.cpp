#include <iostream>
using namespace std;

int main() {
    int data[10];

    cout << "Enter 10 integers (space-separated or newline):" << endl;
    for (int i = 0; i < 10; i++) cin >> data[i];

    cout << "Data items in original order" << endl;
    for (int i = 0; i < 10; i++) cout << data[i] << (i==9?"":" ");
    cout << endl << endl;

    for (int pass = 1; pass <= 9; pass++) {
        bool swapped = false;
        for (int j = 0; j < 10 - pass; j++) {
            if (data[j] > data[j+1]) { 
                int tmp = data[j];
                data[j] = data[j+1];
                data[j+1] = tmp;
                swapped = true;
            }
        }

        cout << "After Pass " << pass << ": ";
        for (int i = 0; i < 10; i++) cout << data[i] << (i==9?"":" ");
        cout << endl;

        if (!swapped) break; 
    }

    cout << endl << "Data items in ascending order" << endl;
    for (int i = 0; i < 10; i++) cout << data[i] << (i==9?"":" ");
    cout << endl;

    return 0;
}
