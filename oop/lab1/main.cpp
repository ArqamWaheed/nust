
#include <iostream>
using namespace std;

struct Student {
    int studentID;
    char studentName[30];
    char department[30];
    float marks;
};

void inputStudents(Student *ptr, int n) {
    for(int i = 0; i < n; i++) {
        cout << "\nStudent " << i+1 << ":\n";
        cout << "Enter Student ID: ";
        cin >> (ptr + i)->studentID;
        cout << "Enter Student Name: ";
        cin >> (ptr + i)->studentName;
        cout << "Enter Department: ";
        cin >> (ptr + i)->department;
        cout << "Enter Marks: ";
        cin >> (ptr + i)->marks;
    }
}

void displayStudents(Student *ptr, int n) {
    cout << "\n--- Student Records ---\n";
    for(int i = 0; i < n; i++) {
        cout << "ID: " << (ptr + i)->studentID << ", Name: " << (ptr + i)->studentName << ", Dept: " << (ptr + i)->department << ", Marks: " << (ptr + i)->marks << endl;
    }
}

float calcAverage(Student *ptr, int n) {
    float total = 0;
    for(int i = 0; i < n; i++)
        total += (ptr + i)->marks;
    return total / n;
}

int main() {
    Student s[5];
    inputStudents(s, 5);
    displayStudents(s, 5);
    cout << "\nAverage Marks: " << calcAverage(s, 5) << endl;
    return 0;
}