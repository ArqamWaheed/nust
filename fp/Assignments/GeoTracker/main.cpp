#include <iostream>
#include <string>
#include <cmath>
using namespace std;

int main() {
    char proceed;
    int studentsChecked = 0, studentsPresent = 0, studentsAbsent = 0;
    do {
        string username;
        float latitude, longitude, inputLatitude, inputLongitude;
        latitude = 33.64373;
        longitude = 72.99198; // NUST's latitude and longitude

        cout << "Enter your username: ";
        cin.ignore(); // Clears any issue previously
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
        distance = sqrt((pow((longitude - inputLongitude), 2) + pow((latitude - inputLatitude), 2)));
        cout << "Your distance is: " << distance << endl;

        // Task 3 beginning now 

        float maxRadius = 0.5;
        if (distance > maxRadius) {
            cout << "You are absent!" << endl;
            studentsAbsent++;
        } else {
            cout << "You are present!" << endl;
            studentsPresent++;
        }

        cout << "Enter y if you want to continue or n if you don't: ";
        cin >> proceed;
        while (proceed != 'n' && proceed != 'y') { // Input validation
            cout << "\ncin failed: Enter either y or n: ";
            cin >> proceed;
        }
        studentsChecked++;
    } while(proceed != 'n');
    cout << "Number of students checked: " << studentsChecked << endl;
    cout << "Number of students present: " << studentsPresent << endl;
    cout << "Number of students absent: " << studentsAbsent << endl;

    return 0;   
}