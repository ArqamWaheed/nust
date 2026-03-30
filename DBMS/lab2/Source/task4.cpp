#include <iostream>
#include <fstream>
using namespace std;

int main() {
    int numArrays;
    cout << "How many arrays to store? ";
    cin >> numArrays;
    
    int** allArrays = new int*[numArrays];
    int* sizes = new int[numArrays];
    
    for(int a = 0; a < numArrays; a++) {
        cout << "\n--- Array " << a+1 << " ---\n";
        cout << "Size: ";
        cin >> sizes[a];
        
        allArrays[a] = new int[sizes[a]];
        cout << "Enter values:\n";
        for(int i = 0; i < sizes[a]; i++) {
            cout << "Val " << i+1 << ": ";
            cin >> allArrays[a][i];
        }
    }
    
    ofstream bout("task4_multi.dat", ios::binary);
    bout.write((char*)&numArrays, sizeof(int));
    for(int a = 0; a < numArrays; a++) {
        bout.write((char*)&sizes[a], sizeof(int));
        bout.write((char*)allArrays[a], sizes[a] * sizeof(int));
    }
    bout.close();
    cout << "\nAll arrays saved to binary!\n";
    
    ifstream bin("task4_multi.dat", ios::binary);
    int totalArrays;
    bin.read((char*)&totalArrays, sizeof(int));
    
    cout << "\n========== Retrieved ==========\n";
    for(int a = 0; a < totalArrays; a++) {
        int sz;
        bin.read((char*)&sz, sizeof(int));
        
        int* tempArr = new int[sz];
        bin.read((char*)tempArr, sz * sizeof(int));
        
        cout << "Array #" << a+1 << ": ";
        for(int i = 0; i < sz; i++) {
            cout << tempArr[i] << " ";
        }
        cout << endl;
        
        delete[] tempArr;
    }
    bin.close();
    
    for(int a = 0; a < numArrays; a++) {
        delete[] allArrays[a];
    }
    delete[] allArrays;
    delete[] sizes;
    
    return 0;
}
