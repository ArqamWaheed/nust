#include <iostream>
#include <string>
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

    cout << "Your username is " << username << "\nYour latitude is: " << inputLatitude << "\nYour longitude is: " << inputLongitude << endl;
    return 0;  
}