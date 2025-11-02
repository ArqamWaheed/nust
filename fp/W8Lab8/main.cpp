#include <iostream>

void calculateSquare(int &num);

int main() {
    int number;
    std::cout << "Enter a number: ";
    std::cin >> number;
    calculateSquare(number);
    std::cout << "The square of the number is: " << number << std::endl;
    return 0;
}

void calculateSquare(int &num) {
    num = num * num;
}