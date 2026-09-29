#include <iostream>
using namespace std;

// a) receives the addresses of a and b
void swapByAddress(int *x, int *y) {
    int temp = *x;
    *x = *y;
    *y = temp;
}

// b) receives ppa and ppb, so two dereferences are needed to reach a and b
void swapByDoublePointer(int **x, int **y) {
    int temp = **x;
    **x = **y;
    **y = temp;
}

int main() {
    int a = 5, b = 10;
    int *pa = &a;       // pa and pb are pointer variables of type int
    int *pb = &b;
    int **ppa = &pa;    // ppa and ppb are pointers-to-pointers
    int **ppb = &pb;

    cout << "Initially:                      a = " << a << ", b = " << b << endl;

    swapByAddress(&a, &b);
    cout << "After swapByAddress(&a, &b):    a = " << a << ", b = " << b << endl;

    swapByDoublePointer(ppa, ppb);
    cout << "After swapByDoublePointer(ppa, ppb): a = " << a << ", b = " << b << endl;

    return 0;
}
