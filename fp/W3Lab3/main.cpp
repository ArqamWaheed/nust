#include <iostream>
using namespace std;

int main() {
    int input1, input2;
    cout << "Enter two numbers to compare: ";
    cin >> input1 >> input2;
    
    cout << "Greater number is: " << (input1 > input2) * input1 + (input2 > input1) * input2 + (input1 == input2) * input1 << endl;
    
    return 0;
}