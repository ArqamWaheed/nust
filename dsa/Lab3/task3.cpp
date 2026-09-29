#include <iostream>
using namespace std;

struct Node {
    int data;
    Node *next;
};

Node *head = nullptr;

void insertAtHead(int value) {
    Node *newNode = new Node;
    newNode->data = value;
    newNode->next = head;
    head = newNode;
    cout << value << " inserted at head." << endl;
}

int countNodes() {
    int count = 0;
    for (Node *current = head; current != nullptr; current = current->next)
        count++;
    return count;
}

void displayList() {
    if (head == nullptr) {
        cout << "List is empty (head -> NULL)" << endl;
        return;
    }
    cout << "head -> ";
    for (Node *current = head; current != nullptr; current = current->next)
        cout << current->data << " -> ";
    cout << "NULL" << endl;
}

void insertAtThird(int value) {
    Node *newNode = new Node;
    newNode->data = value;
    newNode->next = nullptr;

    if (head == nullptr) {
        head = newNode;
        cout << "List was empty, " << value << " inserted at position 1." << endl;
        return;
    }

    Node *second = head->next;
    if (second == nullptr) {
        head->next = newNode;
        cout << "List had only 1 node, " << value << " inserted at the end." << endl;
        return;
    }

    newNode->next = second->next;
    second->next = newNode;
    cout << value << " inserted at position 3." << endl;
}

void deleteLast() {
    if (head == nullptr) {
        cout << "List is empty, nothing to delete." << endl;
        return;
    }

    if (head->next == nullptr) {
        cout << "Deleted " << head->data << ", list is now empty." << endl;
        delete head;
        head = nullptr;
        return;
    }

    Node *current = head;
    while (current->next->next != nullptr)
        current = current->next;

    cout << "Deleted " << current->next->data << " from the end." << endl;
    delete current->next;
    current->next = nullptr;
}

void reverseList() {
    Node *previous = nullptr;
    Node *current = head;

    while (current != nullptr) {
        Node *nextNode = current->next;
        current->next = previous;
        previous = current;
        current = nextNode;
    }
    head = previous;
    cout << "List reversed." << endl;
}

void searchValue(int value) {
    int position = 1;
    for (Node *current = head; current != nullptr; current = current->next) {
        if (current->data == value) {
            cout << value << " found at position " << position << "." << endl;
            return;
        }
        position++;
    }
    cout << value << " is not in the list." << endl;
}

void destroyList() {
    while (head != nullptr) {
        Node *nextNode = head->next;
        delete head;
        head = nextNode;
    }
}

void showMenu() {
    cout << "\n--- Singly Linked List ---" << endl;
    cout << "1. Insert at head" << endl;
    cout << "2. Insert at 3rd position" << endl;
    cout << "3. Display list" << endl;
    cout << "4. Delete last node" << endl;
    cout << "5. Count nodes" << endl;
    cout << "6. Reverse list" << endl;
    cout << "7. Search a value" << endl;
    cout << "8. Exit" << endl;
    cout << "Choice: ";
}

int main() {
    int choice, value;

    while (true) {
        showMenu();

        if (!(cin >> choice)) {
            cin.clear();
            cin.ignore(1000, '\n');
            cout << "Please enter a number between 1 and 8." << endl;
            continue;
        }

        switch (choice) {
        case 1:
            cout << "Value to insert: ";
            cin >> value;
            insertAtHead(value);
            displayList();
            break;
        case 2:
            cout << "Value to insert: ";
            cin >> value;
            insertAtThird(value);
            displayList();
            break;
        case 3:
            displayList();
            break;
        case 4:
            deleteLast();
            displayList();
            break;
        case 5:
            cout << "The list has " << countNodes() << " node(s)." << endl;
            break;
        case 6:
            reverseList();
            displayList();
            break;
        case 7:
            cout << "Value to search: ";
            cin >> value;
            searchValue(value);
            break;
        case 8:
            destroyList();
            cout << "List destroyed, exiting." << endl;
            return 0;
        default:
            cout << "Please enter a number between 1 and 8." << endl;
        }
    }
}
