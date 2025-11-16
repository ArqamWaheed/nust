#include <iostream>
#include <string>
using namespace std;

// Product storage (Ibrahim)
string productNames[100];
float productPrices[100];
int productStock[100];
int productCount = 0;

// Order storage (Arqam)
int orderIndex[100];
int orderQty[100];
int orderCount = 0;

// Product management (Ibrahim)
void addProduct();
void viewProducts();

// Order handling (Arqam)
void placeOrder();

// Billing (Babar)
float getSubtotal();
float getDiscount(float subtotal);
float getTax(float afterDiscount);
void showBill();

int main() {
    while (true) {
        cout << endl << "===== MENU =====" << endl;
        cout << "1. Add Product" << endl;
        cout << "2. View Products" << endl;
        cout << "3. Place Order" << endl;
        cout << "4. Show Bill" << endl;
        cout << "5. Exit" << endl;
        cout << "Choose: ";

        int ch;
        cin >> ch;

        if (ch == 1) addProduct();
        else if (ch == 2) viewProducts();
        else if (ch == 3) placeOrder();
        else if (ch == 4) showBill();
        else if (ch == 5) break;
    else cout << "Invalid choice." << endl;
    }

    return 0;
}

// Ibrahim
void addProduct() {

}


// Ibrahim
void viewProducts() {

}


// Arqam
void placeOrder() {

}


// Babar
float getSubtotal() {

    return 0;
}


// Babar
float getDiscount(float subtotal) {

    return 0;
}


// Babar
float getTax(float afterDiscount) {

    return 0;
}


// Babar
void showBill() {

}

