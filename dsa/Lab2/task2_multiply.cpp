#include <iostream>
using namespace std;

// trying to multiply the address stored in pa
int main()
{
    int a, *pa;
    pa = &a;
    cout<<"pa = &a --> pa = "<<pa<<endl<<endl;

    pa = pa * 2;
    cout<<"pa = pa * 2 --> pa = "<<pa<<endl<<endl;

    return 0;
}
