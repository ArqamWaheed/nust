#include <iostream>
using namespace std;

int main() {
    float length, breadth;

    cout << "Enter length and breadth: ";
    cin >> length >> breadth;

    float area = length * breadth;
    float perimeter = 2 * (length + breadth);

    if (area > perimeter) {
        cout << "Area is greater than perimeter." << endl;
    } else {
        cout << "Area is not greater than perimeter." << endl;
    }
    
    return 0;
}