#include <iostream>
#include <fstream>
using namespace std;

int main() {
    int intCount;
    cout << "How many integers? ";
    cin >> intCount;
    
    int* intArr = new int[intCount];
    cout << "Enter integers:\n";
    for(int i = 0; i < intCount; i++) {
        cout << "Int " << i+1 << ": ";
        cin >> intArr[i];
    }
    
    int floatCount;
    cout << "\nHow many floats? ";
    cin >> floatCount;
    
    float* floatArr = new float[floatCount];
    cout << "Enter floats:\n";
    for(int i = 0; i < floatCount; i++) {
        cout << "Float " << i+1 << ": ";
        cin >> floatArr[i];
    }
    
    ofstream fout("task2_mixed.txt");
    fout << "INTEGERS" << endl;
    fout << intCount << endl;
    for(int i = 0; i < intCount; i++) {
        fout << intArr[i] << endl;
    }
    fout << "FLOATS" << endl;
    fout << floatCount << endl;
    for(int i = 0; i < floatCount; i++) {
        fout << floatArr[i] << endl;
    }
    fout.close();
    cout << "\nBoth arrays saved!\n";
    
    ifstream fin("task2_mixed.txt");
    string marker;
    int iSize, fSize;
    
    fin >> marker >> iSize;
    int* readInts = new int[iSize];
    for(int i = 0; i < iSize; i++) {
        fin >> readInts[i];
    }
    
    fin >> marker >> fSize;
    float* readFloats = new float[fSize];
    for(int i = 0; i < fSize; i++) {
        fin >> readFloats[i];
    }
    fin.close();
    
    cout << "\n=== Retrieved Data ===\n";
    cout << "Integers:\n";
    for(int i = 0; i < iSize; i++) {
        cout << "  [" << i << "] = " << readInts[i] << endl;
    }
    cout << "Floats:\n";
    for(int i = 0; i < fSize; i++) {
        cout << "  [" << i << "] = " << readFloats[i] << endl;
    }
    
    delete[] intArr;
    delete[] floatArr;
    delete[] readInts;
    delete[] readFloats;
    
    return 0;
}
