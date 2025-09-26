#include <iostream>
using namespace std;

int main() {
    int input1, input2, input3;
    
    cout << "Enter three integers: ";
    cin >> input1 >> input2 >> input3;

    bool pos1 = (input1 > 0);
    bool pos2 = (input2 > 0);
    bool pos3 = (input3 > 0);
    
    bool exactlyOnePositive = (pos1 && !pos2 && !pos3) || (!pos1 && pos2 && !pos3) || (!pos1 && !pos2 && pos3);
    
    cout << exactlyOnePositive;
    
    return 0;
}