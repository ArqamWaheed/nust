#include <iostream>
using namespace std;

int main() {
    int x,y,z;
    int Smallest, Largest;
    cout << "Input three different integers: "; 
    cin >> x >> y >> z;
    Smallest = x;
    Largest = x;
    if (x > y) {
        Smallest = y;
    } else {
        Largest = y;
    }
    if (z > Largest) {
        Largest = z;
    }
    if (Smallest > z) {
        Smallest = z;
    } 

    cout << "\nSmallest is: " <<  Smallest << "\nLargest is: " << Largest << endl;
}