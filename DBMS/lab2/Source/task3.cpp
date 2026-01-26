#include <iostream>
#include <fstream>
using namespace std;

int main() {
    int n;
    cout << "Enter array size: ";
    cin >> n;
    
    int* myArr = new int[n];
    cout << "Enter " << n << " numbers:\n";
    for(int i = 0; i < n; i++) {
        cout << "Num " << i+1 << ": ";
        cin >> myArr[i];
    }
    
    ofstream binOut("task3_binary.dat", ios::binary);
    binOut.write((char*)&n, sizeof(int));
    binOut.write((char*)myArr, n * sizeof(int));
    binOut.close();
    cout << "\nSaved to binary file!\n";
    
    ifstream binIn("task3_binary.dat", ios::binary);
    int loadSize;
    binIn.read((char*)&loadSize, sizeof(int));
    
    int* loadedArr = new int[loadSize];
    binIn.read((char*)loadedArr, loadSize * sizeof(int));
    binIn.close();
    
    cout << "\n--- From Binary File ---\n";
    for(int i = 0; i < loadSize; i++) {
        cout << "Position " << i << ": " << loadedArr[i] << endl;
    }
    
    delete[] myArr;
    delete[] loadedArr;
    
    return 0;
}
