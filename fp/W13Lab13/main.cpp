#include <iostream>
using namespace std;

struct Product {
    int productID;
    char productName[30];
    float price;
    int quantity;
    float totalValue;
};

int main() {
    Product p[4];
    
    for (int i = 0; i < 4; i++) {
        cout << "Enter Product ID: ";
        cin >> p[i].productID;
        cout << "Enter Product name: ";
        cin >> p[i].productName;
        cout << "Enter Price: ";
        cin >> p[i].price;
        cout << "Enter Quantity: ";
        cin >> p[i].quantity;
        
        p[i].totalValue = p[i].price * p[i].quantity;
        cout << endl;
    }
    
    cout << "ID\tName\t\tPrice\tQty\tTotal Value\n";
    cout << "---------------------------------------------------\n";
    for (int i = 0; i < 4; i++) {
        cout << p[i].productID << "\t" << p[i].productName << "\t\t" 
             << p[i].price << "\t" << p[i].quantity << "\t" 
             << p[i].totalValue << "\n";
    }
    
    int maxPrice = 0;
    for (int i = 1; i < 4; i++) {
        if (p[i].price > p[maxPrice].price) maxPrice = i;
    }
    cout << "\nMost Expensive Product: " << p[maxPrice].productName 
         << " (Price: " << p[maxPrice].price << ")\n";
    
    int maxValue = 0;
    for (int i = 1; i < 4; i++) {
        if (p[i].totalValue > p[maxValue].totalValue) maxValue = i;
    }
    cout << "Product With Largest Stock Value: " << p[maxValue].productName 
         << " (Total Value: " << p[maxValue].totalValue << ")\n";
    
    return 0;
}
