#include <iostream>
using namespace std;

struct Student {
    char name[20];
    int rollNo;
    float marks1, marks2, marks3;
    float total, percentage;
};

int main() {
    Student s[5];
    
    for (int i = 0; i < 5; i++) {
        cout << "Enter name: ";
        cin >> s[i].name;
        cout << "Enter roll no: ";
        cin >> s[i].rollNo;
        cout << "Enter marks for subject 1: ";
        cin >> s[i].marks1;
        cout << "Enter marks for subject 2: ";
        cin >> s[i].marks2;
        cout << "Enter marks for subject 3: ";
        cin >> s[i].marks3;
        
        s[i].total = s[i].marks1 + s[i].marks2 + s[i].marks3;
        s[i].percentage = s[i].total / 3;
        cout << endl;
    }
    
    cout << "\nStudent Details:\n";
    for (int i = 0; i < 5; i++) {
        cout << "Name: " << s[i].name << ", Roll: " << s[i].rollNo 
             << ", Total: " << s[i].total << ", Percentage: " << s[i].percentage << "%\n";
    }
    
    int best = 0;
    for (int i = 1; i < 5; i++) {
        if (s[i].percentage > s[best].percentage) best = i;
    }
    
    cout << "\nStudent with highest percentage: " << s[best].name 
         << " (" << s[best].percentage << "%)\n";
    
    return 0;
}
