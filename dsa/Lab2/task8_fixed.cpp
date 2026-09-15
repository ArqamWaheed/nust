#include <iostream>
using namespace std;

int main() {
    int n = 3;
    int* values = new int[n];

    // valid indexes are 0 to n-1, so the condition is i < n
    cout << "Enter " << n << " integers: ";
    for (int i = 0; i < n; i++)
        cin >> values[i];

    // display before releasing the memory
    cout << "Values: ";
    for (int i = 0; i < n; i++)
        cout << values[i] << " ";
    cout << endl;

    delete[] values;    // memory from new[] is released with delete[]
    values = nullptr;   // values no longer points to freed memory

    return 0;
}
