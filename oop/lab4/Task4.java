class Stack {
    int arr[];
    int top;

    Stack() {
        arr = new int[10];
        top = -1;
    }

    void push(int val) {
        if(top >= 9) {
            System.out.println("Stack Overflow!");
        }
        else {
            top++;
            arr[top] = val;
        }
    }

    int pop() {
        if(top < 0) {
            System.out.println("Stack Underflow!");
            return -1;
        }
        else {
            int val = arr[top];
            top--;
            return val;
        }
    }

    void display() {
        if(top < 0) {
            System.out.println("Empty Stack");
        }
        else {
            System.out.print("Current Stack: ");
            int i = 0;
            while(i <= top) {
                System.out.print(arr[i] + " ");
                i++;
            }
            System.out.println();
        }
    }
}

public class Task4 {
    public static void main(String args[]) {
        Stack s = new Stack();

        System.out.println("Adding 5 elements: 15, 25, 35, 45, 55");
        s.push(15);
        s.push(25);
        s.push(35);
        s.push(45);
        s.push(55);
        s.display();

        System.out.println();
        int popped = s.pop();
        System.out.println("Popped: " + popped);
        s.display();

        System.out.println();
        popped = s.pop();
        System.out.println("Popped: " + popped);
        s.display();

        System.out.println();
        System.out.println("Adding 65, 75");
        s.push(65);
        s.push(75);
        s.display();

        System.out.println();
        System.out.println("Testing overflow by adding more elements:");
        s.push(85);
        s.push(95);
        s.push(105);
        s.push(115);
        s.push(125);
        s.display();
    }
}
