#include <iostream>
#include <fstream>
using namespace std;

int main() {
    int numArrays;
    cout << "How many arrays to store? ";
    cin >> numArrays;
    
    ofstream bout("task5_arrays.dat", ios::binary);
    bout.write((char*)&numArrays, sizeof(int));
    
    for(int a = 0; a < numArrays; a++) {
        cout << "\n--- Array " << a+1 << " ---\n";
        int sz;
        cout << "Size: ";
        cin >> sz;
        
        int* arr = new int[sz];
        cout << "Enter values:\n";
        for(int i = 0; i < sz; i++) {
            cout << "Value " << i+1 << ": ";
            cin >> arr[i];
        }
        
        bout.write((char*)&sz, sizeof(int));
        bout.write((char*)arr, sz * sizeof(int));
        
        delete[] arr;
    }
    bout.close();
    cout << "\nAll arrays saved to binary file!\n";
    
    int choice;
    cout << "\nWhich array to retrieve (1 to " << numArrays << ")? ";
    cin >> choice;
    
    ifstream bin("task5_arrays.dat", ios::binary);
    int total;
    bin.read((char*)&total, sizeof(int));
    
    if(choice < 1 || choice > total) {
        cout << "Invalid selection!\n";
        return 1;
    }
    
    for(int a = 1; a <= total; a++) {
        int sz;
        bin.read((char*)&sz, sizeof(int));
        
        if(a == choice) {
            int* arr = new int[sz];
            bin.read((char*)arr, sz * sizeof(int));
            
            cout << "\nArray " << choice << " data:\n";
            for(int i = 0; i < sz; i++) {
                cout << arr[i] << " ";
            }
            cout << endl;
            
            delete[] arr;
            break;
        } else {
            bin.seekg(sz * sizeof(int), ios::cur);
        }
    }
    bin.close();
    
    return 0;
}
