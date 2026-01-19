
#include<iostream>
using namespace std;

void printArray(int *p, int size){
    cout<<"Array elements: ";
    for(int i=0; i<size; i++){
        cout<<*(p+i)<<" ";
    }
    cout<<endl;
}

int main(){
    int arr[] = {10, 20, 30, 40, 50};
    int size = 5;
    printArray(arr, size);
    return 0;
}