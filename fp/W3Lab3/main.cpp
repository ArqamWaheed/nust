#include <iostream>
using namespace std;

int main() {
    float distanceKm;

    cout << "Enter distance between two cities (in km): ";
    cin >> distanceKm;
    
    float meters = distanceKm * 1000;              
    float feet = distanceKm * 3280.84;                  
    float inches = distanceKm * 39370.1;                
    float centimeters = distanceKm * 100000;        
    
    cout << "Distance in Kilometers: " << distanceKm << " km" << endl;
    cout << "Distance in Meters:     " << meters << " m" << endl;
    cout << "Distance in Feet:       " << feet << " ft" << endl;
    cout << "Distance in Inches:     " << inches << " in" << endl;
    cout << "Distance in Centimeters: " << centimeters << " cm" << endl;
    
    return 0;
}   