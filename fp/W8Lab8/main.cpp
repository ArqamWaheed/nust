#include <iostream>
using namespace std;


void area(); // Function prototype defined here

int main()
{
    area();
    return 0;
}

void area() // Function definition here.
{
    float area;
    float radius;
    cout << "Enter the radius : ";
    cin >> radius;
    area = 3.14f * radius * radius;
    cout << "Area of Circle = " << area << endl;
}