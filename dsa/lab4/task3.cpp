#include <iostream>
#include <string>
using namespace std;

struct BitNode {
    int bit;
    BitNode* prev;
    BitNode* next;

    BitNode(int b) {
        bit = b;
        prev = nullptr;
        next = nullptr;
    }
};

// one binary number, head is the most significant bit and tail the least
// the length is always kept a multiple of 8 so it splits into 8-bit blocks
class Binary {
public:
    BitNode* head;
    BitNode* tail;
    int length;

    Binary() {
        head = tail = nullptr;
        length = 0;
    }

    ~Binary() {
        clear();
    }

    // copying would share the same nodes and delete them twice, so it's blocked
    Binary(const Binary&) = delete;
    Binary& operator=(const Binary&) = delete;

    void clear() {
        while (head != nullptr) {
            BitNode* doomed = head;
            head = head->next;
            delete doomed;
        }
        tail = nullptr;
        length = 0;
    }

    // new bit becomes the least significant one
    void pushBack(int b) {
        BitNode* fresh = new BitNode(b);
        if (tail == nullptr)
            head = tail = fresh;
        else {
            tail->next = fresh;
            fresh->prev = tail;
            tail = fresh;
        }
        length++;
    }

    // new bit becomes the most significant one
    void pushFront(int b) {
        BitNode* fresh = new BitNode(b);
        if (head == nullptr)
            head = tail = fresh;
        else {
            fresh->next = head;
            head->prev = fresh;
            head = fresh;
        }
        length++;
    }

    void popFront() {
        BitNode* doomed = head;
        head = head->next;
        if (head != nullptr)
            head->prev = nullptr;
        else
            tail = nullptr;
        delete doomed;
        length--;
    }

    // zeros in front until the length is a whole number of 8-bit blocks
    void padTo8() {
        if (length == 0)
            pushFront(0);
        while (length % 8 != 0)
            pushFront(0);
    }

    // drops leading zero blocks, keeps at least one block
    void trim() {
        while (length > 8 && head->bit == 0) {
            // only drop a whole block if all 8 of its bits are 0
            BitNode* cur = head;
            bool allZero = true;
            for (int i = 0; i < 8; i++, cur = cur->next)
                if (cur->bit != 0)
                    allZero = false;
            if (!allZero)
                break;
            for (int i = 0; i < 8; i++)
                popFront();
        }
    }

    void display() const {
        int i = 0;
        for (BitNode* cur = head; cur != nullptr; cur = cur->next) {
            cout << cur->bit;
            i++;
            if (i % 8 == 0 && cur->next != nullptr)
                cout << " ";
        }
        cout << "  (" << length / 8 << (length == 8 ? " block)" : " blocks)");
    }
};

// Store Binary Number: every character becomes one node, then padded to 8-bit blocks
bool storeBinary(Binary &num, const string &bits) {
    if (bits.empty())
        return false;
    for (int i = 0; i < (int)bits.length(); i++)
        if (bits[i] != '0' && bits[i] != '1')
            return false;

    num.clear();
    for (int i = 0; i < (int)bits.length(); i++)
        num.pushBack(bits[i] - '0');
    num.padTo8();
    return true;
}

void copyBinary(const Binary &src, Binary &dest) {
    dest.clear();
    for (BitNode* cur = src.head; cur != nullptr; cur = cur->next)
        dest.pushBack(cur->bit);
}

// 1's complement: walk the list once and flip every bit in place
void onesComplement(Binary &num) {
    for (BitNode* cur = num.head; cur != nullptr; cur = cur->next)
        cur->bit = 1 - cur->bit;
}

// 2's complement: flip everything, then add 1 starting from the tail
// carry keeps moving left through prev pointers, a carry out of the
// leftmost bit is dropped because the width stays the same
void twosComplement(Binary &num) {
    onesComplement(num);

    int carry = 1;
    for (BitNode* cur = num.tail; cur != nullptr && carry == 1; cur = cur->prev) {
        int sum = cur->bit + carry;
        cur->bit = sum % 2;
        carry = sum / 2;
    }
}

// Binary Addition: both lists are walked from the tail (LSB) using prev
// each result bit is pushed to the front of the answer
void addBinary(const Binary &a, const Binary &b, Binary &result) {
    result.clear();

    BitNode* x = a.tail;
    BitNode* y = b.tail;
    int carry = 0;

    while (x != nullptr || y != nullptr || carry != 0) {
        int sum = carry;
        if (x != nullptr) {
            sum += x->bit;
            x = x->prev;
        }
        if (y != nullptr) {
            sum += y->bit;
            y = y->prev;
        }
        result.pushFront(sum % 2);
        carry = sum / 2;
    }

    // a final carry can make it 9 bits, padding adds a new 8-bit block
    result.padTo8();
    result.trim();
}

// Binary Multiplication: shift and add
// for every 1 in b (starting from the LSB), a shifted left by that
// position is added to the running total. shifting = zeros at the tail
void multiplyBinary(const Binary &a, const Binary &b, Binary &result) {
    Binary total, shifted, temp;
    storeBinary(total, "0");
    copyBinary(a, shifted);

    for (BitNode* cur = b.tail; cur != nullptr; cur = cur->prev) {
        if (cur->bit == 1) {
            addBinary(total, shifted, temp);    // repeated addition
            copyBinary(temp, total);
        }
        shifted.pushBack(0);                    // shift left by one
    }

    copyBinary(total, result);
    result.padTo8();
    result.trim();
}

// Conversion to Decimal: from the MSB, value = value * 2 + bit
unsigned long long toDecimal(const Binary &num) {
    unsigned long long value = 0;
    for (BitNode* cur = num.head; cur != nullptr; cur = cur->next)
        value = value * 2 + cur->bit;
    return value;
}

// the same bits read as a signed (2's complement) number
long long toSignedDecimal(const Binary &num) {
    unsigned long long value = toDecimal(num);
    if (num.head->bit == 1 && num.length < 64)
        return (long long)value - (1LL << num.length);
    return (long long)value;
}

// counts bits from the first 1, anything over 64 won't fit in a long long
int significantBits(const Binary &num) {
    int count = num.length;
    for (BitNode* cur = num.head; cur != nullptr && cur->bit == 0; cur = cur->next)
        count--;
    return count;
}

void printDecimal(const Binary &num) {
    if (significantBits(num) > 64) {
        cout << "too large to fit in 64 bits";
        return;
    }
    cout << toDecimal(num);
}

void printNumber(const string &label, const Binary &num) {
    cout << label;
    if (num.length == 0) {
        cout << "(not stored)" << endl;
        return;
    }
    num.display();
    cout << " = ";
    printDecimal(num);
    cout << endl;
}

void readBinary(const string &label, Binary &num) {
    string bits;
    cout << "Enter binary number " << label << ": ";
    cin >> bits;
    while (!storeBinary(num, bits)) {
        cout << "Only 0s and 1s allowed, enter again: ";
        cin >> bits;
    }
    printNumber("Stored "+label+" = ", num);
}

// asks which number to use for the single-number operations
Binary* pickNumber(Binary &a, Binary &b, string &label) {
    char which;
    cout << "Which number (A/B): ";
    cin >> which;
    if (which == 'a' || which == 'A') {
        label = "A";
        return &a;
    }
    if (which == 'b' || which == 'B') {
        label = "B";
        return &b;
    }
    cout << "Invalid choice" << endl;
    return nullptr;
}

void showMenu() {
    cout << endl;
    cout << "1.Store A  2.Store B  3.1's comp  4.2's comp  5.A+B  6.A*B  7.Decimal  8.Exit" << endl;
    cout << "Enter choice: ";
}

int main() {
    Binary a, b;
    int choice;
    bool running = true;

    while (running) {
        showMenu();
        if (!(cin >> choice)) {
            if (cin.eof())
                break;
            cin.clear();
            cin.ignore(1000, '\n');
            cout << "Invalid choice" << endl;
            continue;
        }

        string label;
        Binary* num;
        Binary result;

        switch (choice) {
            case 1:
                readBinary("A", a);
                break;

            case 2:
                readBinary("B", b);
                break;

            case 3:
                num = pickNumber(a, b, label);
                if (num == nullptr)
                    break;
                if (num->length == 0) {
                    cout << label << " is not stored yet" << endl;
                    break;
                }
                copyBinary(*num, result);
                onesComplement(result);
                printNumber(label+"        = ", *num);
                printNumber("1's comp = ", result);
                break;

            case 4:
                num = pickNumber(a, b, label);
                if (num == nullptr)
                    break;
                if (num->length == 0) {
                    cout << label << " is not stored yet" << endl;
                    break;
                }
                copyBinary(*num, result);
                twosComplement(result);
                printNumber(label+"        = ", *num);
                printNumber("2's comp = ", result);
                if (result.length < 64)
                    cout << "As a signed " << result.length << "-bit number: "
                        << toSignedDecimal(result) << endl;
                break;

            case 5:
                if (a.length == 0 || b.length == 0) {
                    cout << "Store both A and B first" << endl;
                    break;
                }
                addBinary(a, b, result);
                printNumber("A     = ", a);
                printNumber("B     = ", b);
                printNumber("A + B = ", result);
                break;

            case 6:
                if (a.length == 0 || b.length == 0) {
                    cout << "Store both A and B first" << endl;
                    break;
                }
                multiplyBinary(a, b, result);
                printNumber("A     = ", a);
                printNumber("B     = ", b);
                printNumber("A * B = ", result);
                break;

            case 7:
                num = pickNumber(a, b, label);
                if (num == nullptr)
                    break;
                if (num->length == 0) {
                    cout << label << " is not stored yet" << endl;
                    break;
                }
                cout << label << " in decimal = ";
                printDecimal(*num);
                cout << endl;
                break;

            case 8:
                running = false;
                break;

            default:
                cout << "Invalid choice" << endl;
        }
    }
    cout << "Exiting" << endl;
}
