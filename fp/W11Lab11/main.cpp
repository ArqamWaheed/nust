#include <iostream>
using namespace std;

int main() {
    int arr[10];

    cout << "Enter 10 numbers (speerate with space):" << endl;
    for (int i = 0; i < 10; i++) {
        cin >> arr[i];
    }

    for (int pass = 0; pass < 9; pass++) {
        for (int j = 0; j < 9 - pass; j++) {
            if (arr[j] < arr[j+1]) { 
                int tmp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = tmp;
            }
        }
    }

    cout << "Sorted data (descending):" << endl;
    for (int i = 0; i < 10; i++) cout << arr[i] << " ";
    cout << endl;

    return 0;
}
