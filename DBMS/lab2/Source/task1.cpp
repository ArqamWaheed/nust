#include <iostream>
#include <fstream>
using namespace std;

int main() {
    int n;
    cout << "Enter how many numbers you want: ";
    cin >> n;
    
    int* arr = new int[n];
    
    cout << "Enter " << n << " integers:\n";
    for(int i = 0; i < n; i++) {
        cout << "Number " << i+1 << ": ";
        cin >> arr[i];
    }
    
    ofstream outFile("task1_data.txt");
    outFile << n << endl;
    for(int i = 0; i < n; i++) {
        outFile << arr[i] << endl;
    }
    outFile.close();
    cout << "\nData saved to task1_data.txt\n";
    
    ifstream inFile("task1_data.txt");
    int size;
    inFile >> size;
    
    int* loadedArr = new int[size];
    for(int i = 0; i < size; i++) {
        inFile >> loadedArr[i];
    }
    inFile.close();
    
    cout << "\n--- Data from file ---\n";
    for(int i = 0; i < size; i++) {
        cout << "Element " << i+1 << ": " << loadedArr[i] << endl;
    }
    
    delete[] arr;
    delete[] loadedArr;
    
    return 0;
}
