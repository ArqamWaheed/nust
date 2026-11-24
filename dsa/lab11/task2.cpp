#include <iostream>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int v) {
        val = v;
        next = nullptr;
    }
};

// binary min heap that stores list nodes, ordered by val
struct MinHeap {
    ListNode* a[100];
    int size;
    MinHeap() {
        size = 0;
    }
    void swapAt(int i, int j) {
        ListNode* t = a[i];
        a[i] = a[j];
        a[j] = t;
    }
    void push(ListNode* n) {
        a[size] = n;
        int i = size++;
        while (i > 0 && a[i]->val < a[(i - 1) / 2]->val) {
            swapAt(i, (i - 1) / 2);
            i = (i - 1) / 2;
        }
    }
    ListNode* pop() {
        ListNode* top = a[0];
        a[0] = a[--size];
        int i = 0;
        while (true) {
            int l = 2 * i + 1, r = 2 * i + 2, m = i;
            if (l < size && a[l]->val < a[m]->val)
                m = l;
            if (r < size && a[r]->val < a[m]->val)
                m = r;
            if (m == i)
                break;
            swapAt(i, m);
            i = m;
        }
        return top;
    }
};

// heap only ever holds the current head of each list, so it has at most k nodes
ListNode* mergeKLists(ListNode* lists[], int k) {
    MinHeap h;
    for (int i = 0; i < k; i++)
        if (lists[i] != nullptr)
            h.push(lists[i]);
    ListNode dummy(0);
    ListNode* tail = &dummy;
    while (h.size > 0) {
        ListNode* smallest = h.pop();
        tail->next = smallest;   // relink the existing node, no copies
        tail = smallest;
        if (smallest->next != nullptr)
            h.push(smallest->next);
    }
    tail->next = nullptr;
    return dummy.next;
}

ListNode* build(int arr[], int n) {
    ListNode* head = nullptr;
    for (int i = n - 1; i >= 0; i--) {
        ListNode* node = new ListNode(arr[i]);
        node->next = head;
        head = node;
    }
    return head;
}

void print(ListNode* head) {
    cout << "[";
    for (ListNode* p = head; p != nullptr; p = p->next)
        cout << p->val << (p->next ? " -> " : "");
    cout << "]" << endl;
}

void freeList(ListNode* head) {
    while (head != nullptr) {
        ListNode* d = head;
        head = head->next;
        delete d;
    }
}

void solve(ListNode* lists[], int k) {
    for (int i = 0; i < k; i++) {
        cout << "list " << i + 1 << ": ";
        print(lists[i]);
    }
    ListNode* merged = mergeKLists(lists, k);
    cout << "merged: ";
    print(merged);
    cout << endl;
    freeList(merged);
}

int main() {
    int a[] = {1, 4, 5}, b[] = {1, 3, 4}, c[] = {2, 6};
    ListNode* lists1[] = {build(a, 3), build(b, 3), build(c, 2)};
    solve(lists1, 3);

    int d[] = {-3, 0, 8, 15}, e[] = {2, 2, 9}, g[] = {-7, 20}, h[] = {5};
    ListNode* lists2[] = {build(d, 4), nullptr, build(e, 3), build(g, 2), build(h, 1)};
    solve(lists2, 5);

    ListNode* lists3[] = {nullptr, nullptr};
    solve(lists3, 2);
    return 0;
}
