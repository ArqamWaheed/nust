import java.util.Scanner;

// task 4 - reverse array and check if its a palindrome
public class Task4 {
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("How many integers do you want to enter? ");
        int n = scanner.nextInt();
        
        if (n <= 0) {
            System.out.println("Invalid size! Exiting...");
            scanner.close();
            return;
        }
        
        int[] array = new int[n];
        
        System.out.println("\nEnter " + n + " integers:");
        for (int i = 0; i < n; i++) {
            System.out.print("  Element [" + i + "]: ");
            array[i] = scanner.nextInt();
        }
        
        System.out.println("\n--- Results ---");
        
        System.out.print("Original Array: ");
        printArray(array);
        
        int[] reversedArr = reverseArray(array);
        
        System.out.print("Reversed Array: ");
        printArray(reversedArr);
        
        boolean palindrome = isPalindrome(array);
        
        System.out.println();
        if (palindrome) {
            System.out.println(">> The array IS a palindrome! <<");
        } else {
            System.out.println(">> The array is NOT a palindrome. <<");
        }
        
        scanner.close();
    }
    
    // returns reversed array
    public static int[] reverseArray(int[] array) {
        int len = array.length;
        int[] reversed = new int[len];
        
        for (int i = 0; i < len; i++) {
            reversed[i] = array[len - 1 - i];
        }
        return reversed;
    }
    
    // checks if array is palindrome
    public static boolean isPalindrome(int[] array) {
        int len = array.length;
        
        for (int i = 0; i < len / 2; i++) {
            if (array[i] != array[len - 1 - i]) {
                return false;
            }
        }
        return true;
    }
    
    // prints array elements
    public static void printArray(int[] array) {
        System.out.print("{ ");
        for (int i = 0; i < array.length; i++) {
            System.out.print(array[i]);
            if (i < array.length - 1) {
                System.out.print(", ");
            }
        }
        System.out.println(" }");
    }
}
