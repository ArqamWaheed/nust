#include <iostream>
using namespace std;

int main() {
    int year;
    cout << "Input  an year: "; 
    cin >> year;
    
    if (year % 4 == 0) {
        cout << "This is a leap year";
    } else {
        cout << "This is not a leap year";
    }
}