#include <iostream>
#include <fstream>
using namespace std;

int main() {
    int numArrays;
    cout << "How many arrays do you want to store? ";
    cin >> numArrays;
    
    ofstream fout("task5_arrays.txt");
    fout << numArrays << endl;
    
    for(int a = 0; a < numArrays; a++) {
        cout << "\n--- Array " << a+1 << " ---\n";
        int sz;
        cout << "Enter size: ";
        cin >> sz;
        
        fout << sz << endl;
        
        cout << "Enter elements:\n";
        for(int i = 0; i < sz; i++) {
            int val;
            cout << "Element " << i+1 << ": ";
            cin >> val;
            fout << val << endl;
        }
    }
    fout.close();
    cout << "\nAll arrays saved to text file!\n";
    
    int choice;
    cout << "\nWhich array do you want to read (1 to " << numArrays << ")? ";
    cin >> choice;
    
    ifstream fin("task5_arrays.txt");
    int total;
    fin >> total;
    
    if(choice < 1 || choice > total) {
        cout << "Invalid choice!\n";
        return 1;
    }
    
    for(int a = 1; a <= total; a++) {
        int sz;
        fin >> sz;
        
        if(a == choice) {
            int* arr = new int[sz];
            for(int i = 0; i < sz; i++) {
                fin >> arr[i];
            }
            
            cout << "\nArray " << choice << " contents:\n";
            for(int i = 0; i < sz; i++) {
                cout << arr[i] << " ";
            }
            cout << endl;
            
            delete[] arr;
            break;
        } else {
            int temp;
            for(int i = 0; i < sz; i++) {
                fin >> temp;
            }
        }
    }
    fin.close();
    
    return 0;
}
