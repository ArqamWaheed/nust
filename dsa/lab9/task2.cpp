#include <iostream>
#include <string>
#include <cctype>
using namespace std;

struct WordNode {
    string word;
    int count;
    WordNode* left;
    WordNode* right;
    WordNode(string w) {
        word = w;
        count = 1;
        left = nullptr;
        right = nullptr;
    }
};

class WordBST {
    WordNode* root = nullptr;
    int unique = 0;
    int total = 0;

    WordNode* insert(WordNode* node, const string& w) {
        if (node == nullptr) {
            unique++;
            return new WordNode(w);
        }
        if (w < node->word)
            node->left = insert(node->left, w);
        else if (w > node->word)
            node->right = insert(node->right, w);
        else
            node->count++;
        return node;
    }

    void inorder(WordNode* node) {
        if (node == nullptr)
            return;
        inorder(node->left);
        cout << "  " << node->word << " : " << node->count << "\n";
        inorder(node->right);
    }

    // copies nodes into an array in alphabetical order
    void collect(WordNode* node, WordNode* arr[], int& i) {
        if (node == nullptr)
            return;
        collect(node->left, arr, i);
        arr[i++] = node;
        collect(node->right, arr, i);
    }

    int maxCount(WordNode* node) {
        if (node == nullptr)
            return 0;
        int best = node->count;
        int l = maxCount(node->left);
        int r = maxCount(node->right);
        if (l > best)
            best = l;
        if (r > best)
            best = r;
        return best;
    }

    void printWithCount(WordNode* node, int c) {
        if (node == nullptr)
            return;
        printWithCount(node->left, c);
        if (node->count == c)
            cout << "  " << node->word << " (" << c << ")\n";
        printWithCount(node->right, c);
    }

public:
    // splits on anything that is not a letter and lowercases each word
    void insertParagraph(const string& text) {
        string w;
        for (size_t i = 0; i <= text.size(); i++) {
            if (i < text.size() && isalpha((unsigned char)text[i])) {
                w += tolower((unsigned char)text[i]);
            } else if (!w.empty()) {
                root = insert(root, w);
                total++;
                w = "";
            }
        }
    }

    void displayAlphabetical() {
        cout << "Words in alphabetical order:\n";
        inorder(root);
    }

    void displayByFrequency() {
        WordNode* arr[200];
        int n = 0;
        collect(root, arr, n);
        // insertion sort, stable so equal counts stay alphabetical
        for (int i = 1; i < n; i++) {
            WordNode* cur = arr[i];
            int j = i - 1;
            while (j >= 0 && arr[j]->count < cur->count) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = cur;
        }
        cout << "Words by frequency (highest first):\n";
        for (int i = 0; i < n; i++)
            cout << "  " << arr[i]->word << " : " << arr[i]->count << "\n";
    }

    void findMostFrequentWord() {
        int c = maxCount(root);
        cout << "Most frequent word(s):\n";
        printWithCount(root, c);
    }

    void summary() {
        cout << "Total unique words: " << unique << "\n";
        cout << "Total word count  : " << total << "\n";
    }
};

int main() {
    string text = "The quick brown fox jumps over the lazy dog. The fox is quick and smart.";
    cout << "Paragraph: " << text << "\n\n";
    WordBST bst;
    bst.insertParagraph(text);
    bst.displayAlphabetical();
    cout << "\n";
    bst.displayByFrequency();
    cout << "\n";
    bst.findMostFrequentWord();
    cout << "\n";
    bst.summary();
    return 0;
}
