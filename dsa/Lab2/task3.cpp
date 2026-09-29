#include <iostream>
using namespace std;

int main() {
    int list[5] = {3, 6, 9, 12, 15};
    int *pArr = list;

    // print the value pArr points to, then move it to the next element
    for (int i = 0; i < 5; i++) {
        cout << *pArr << " ";
        pArr++;
    }
    cout << endl;

    return 0;
}
