#include <iostream>
using namespace std;

void iterateArray(int* ptr, int size) {
    int* end = ptr + size;
    
    while (ptr < end) {
        cout << *ptr << " ";
        ptr++;  
    }
    cout << endl;
}

int main() {
    int arr[] = {1, 2, 3, 4, 5};  
    
    cout << "Array elements: ";
    iterateArray(arr, sizeof(arr) / sizeof(arr[0]));
    
    return 0;
}