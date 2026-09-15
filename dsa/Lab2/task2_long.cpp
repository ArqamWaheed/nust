#include <iostream>
using namespace std;

// same program as task2.cpp but with long instead of int
int main()
{
    long a, *pa;    // Statement 1
    pa = &a;        // Statement 2
    cout<<"pa = &a --> pa = "<<pa<<endl<<endl;

    pa = pa + 1;    // Statement 3
    cout<<"pa = pa + 1 --> pa = "<<pa<<endl<<endl;

    pa = pa + 3;    // Statement 4
    cout<<"pa = pa + 3 --> pa = "<<pa<<endl<<endl;

    pa = pa - 1;    // Statement 5
    cout<<"pa = pa - 1 --> pa = "<<pa<<endl<<endl;

    return 0;
}
