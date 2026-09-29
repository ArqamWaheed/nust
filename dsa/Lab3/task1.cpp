#include <iostream>
#include <string>
#include <cctype>
using namespace std;

bool isPalindrome(const string &text) {
    int left = 0;
    int right = (int)text.length() - 1;

    while (left < right) {
        while (left < right && !isalnum((unsigned char)text[left]))
            left++;
        while (left < right && !isalnum((unsigned char)text[right]))
            right--;

        if (tolower((unsigned char)text[left]) != tolower((unsigned char)text[right]))
            return false;

        left++;
        right--;
    }
    return true;
}

int main() {
    string text;
    cout << "Enter a string: ";
    getline(cin, text);

    if (isPalindrome(text))
        cout << "\"" << text << "\" is a palindrome." << endl;
    else
        cout << "\"" << text << "\" is not a palindrome." << endl;

    return 0;
}
