#include <iostream>
#include <string>
#include <cmath>
using namespace std;

int main() {
    string username;
    float latitude, longitude, inputLatitude, inputLongitude;
    latitude = 33.64373;
    longitude = 72.99198; // NUST's latitude and longitude

    cout << "Enter your username: ";
    getline(cin, username);

    cout << "\nEnter your current latitude and longitude respectively: ";
    cin >> inputLatitude >> inputLongitude;
    while (cin.fail()) {
        cout << "\ncin failed: invalid input type! Input properly again!: ";
        cin.clear();
        cin.ignore(10000, '\n');
        cin >> inputLatitude >> inputLongitude;
    }

    cout << "Your username is " << username << "\nYour latitude is: " << inputLatitude << "\nYour longitude is: " << inputLongitude << endl;

    // Task 2 beginning now

    float distance; 
    distance = (pow((longitude - inputLongitude), 2) + pow((latitude - inputLatitude), 2));
    cout << "Your distance is: " << distance << endl;
    return 0;  
}