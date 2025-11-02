#include <iostream>
using namespace std;

// Function prototype now takes float radius and returns float area
float area(float radius);

int main()
{
    float radius;
    cout << "Enter the radius : ";
    cin >> radius;
    // Changed: Pass radius by value, get area back, display in main
    float result = area(radius);
    cout << "Area of Circle = " << result << endl;
    return 0;
}

// Function definition now takes radius parameter, calculates and returns area
float area(float r)
{
    return 3.14f * r * r;
}