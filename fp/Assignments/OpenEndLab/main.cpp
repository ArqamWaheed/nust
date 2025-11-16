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
    if (productCount >= 100) return;

    cout << "Enter product name: ";
    cin.ignore();
    getline(cin, productNames[productCount]);

    cout << "Enter price: ";
    cin >> productPrices[productCount];

    cout << "Enter stock quantity: ";
    cin >> productStock[productCount];

    productCount++;
}

// Ibrahim
void viewProducts() {
    if (productCount == 0) return;

    for (int i = 0; i < productCount; i++) {
        cout << i + 1 << ". " << productNames[i] << " | Price: " << productPrices[i] << " | Stock: " << productStock[i] << endl;
    }
}

// Arqam
void placeOrder() {
    if (productCount == 0) return;

    viewProducts();

    int productNum;
    cout << "Enter product number: ";
    cin >> productNum;

    if (productNum < 1 || productNum > productCount) return;

    int index = productNum - 1;

    int quantity;
    cout << "Enter quantity: ";
    cin >> quantity;

    if (quantity > productStock[index]) return;

    productStock[index] -= quantity;

    orderIndex[orderCount] = index;
    orderQty[orderCount] = quantity;
    orderCount++;
}

// Babar
float getSubtotal() {
    float subtotal = 0;

    for (int i = 0; i < orderCount; i++) {
        int index = orderIndex[i];
        subtotal += productPrices[index] * orderQty[i];
    }

    return subtotal;
}

// Babar
float getDiscount(float subtotal) {
    if (subtotal > 10000) return subtotal * 0.10f;
    if (subtotal > 5000) return subtotal * 0.05f;
    return 0;
}

// Babar
float getTax(float afterDiscount) {
    return afterDiscount * 0.08f;
}

// Babar
void showBill() {
    if (orderCount == 0) return;

    for (int i = 0; i < orderCount; i++) {
        int index = orderIndex[i];
        float totalItem = productPrices[index] * orderQty[i];

        cout << productNames[index] << " | Qty: " << orderQty[i] << " | Price: " << productPrices[index] << " | Total: " << totalItem << endl;
    }

    float subtotal = getSubtotal();
    float discount = getDiscount(subtotal);
    float afterDiscount = subtotal - discount;
    float tax = getTax(afterDiscount);
    float finalTotal = afterDiscount + tax;

    cout << "Subtotal: " << subtotal << endl;
    cout << "Discount: " << discount << endl;
    cout << "After Discount: " << afterDiscount << endl;
    cout << "Tax: " << tax << endl;
    cout << "FINAL TOTAL: " << finalTotal << endl;
}
