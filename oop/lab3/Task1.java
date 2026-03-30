import java.util.Scanner;

// task 1 - swap first and last element
public class Task1 {
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("Enter the size of array: ");
        int n = scanner.nextInt();
        
        if (n < 2) {
            System.out.println("Array must have at least 2 elements to swap!");
            scanner.close();
            return;
        }
        
        int[] arr = new int[n];
        
        System.out.println("Enter " + n + " integers:");
        for (int i = 0; i < n; i++) {
            System.out.print("Element [" + i + "]: ");
            arr[i] = scanner.nextInt();
        }
        
        System.out.print("\nOriginal array: ");
        printArray(arr);
        
        swapFirstAndLast(arr);
        
        System.out.print("After swapping: ");
        printArray(arr);
        
        scanner.close();
    }
    
    // swaps first and last
    public static void swapFirstAndLast(int[] array) {
        int temp = array[0];
        array[0] = array[array.length - 1];
        array[array.length - 1] = temp;
    }
    
    public static void printArray(int[] array) {
        System.out.print("[ ");
        for (int i = 0; i < array.length; i++) {
            System.out.print(array[i]);
            if (i < array.length - 1) {
                System.out.print(", ");
            }
        }
        System.out.println(" ]");
    }
}
