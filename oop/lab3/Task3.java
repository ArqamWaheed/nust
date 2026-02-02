import java.util.Random;
import java.util.Scanner;

// task 3 - array operations using methods
public class Task3 {
    
    static Scanner scanner = new Scanner(System.in);
    static Random random = new Random();
    
    public static void main(String[] args) {
        
        final int N = 10;
        int[] array = new int[N];
        
        populateArray(array, N);
        
        System.out.println("=== Array Operations Demo ===\n");
        
        System.out.println("Original array:");
        printArray(array, N);
        
        sortArray(array, N);
        
        System.out.println("\nAfter sorting:");
        printArray(array, N);
        
        System.out.print("\nEnter element to search: ");
        int searchElement = scanner.nextInt();
        
        boolean found = findElement(array, searchElement);
        
        if (found) {
            System.out.println("Element " + searchElement + " was FOUND in the array!");
        } else {
            System.out.println("Element " + searchElement + " was NOT FOUND in the array.");
        }
        
        scanner.close();
    }
    
    // fills array with random nums 1 to 100
    public static void populateArray(int[] array, int N) {
        for (int i = 0; i < N; i++) {
            array[i] = random.nextInt(100) + 1;
        }
    }
    
    // prints the array
    public static void printArray(int[] array, int N) {
        System.out.print("[ ");
        for (int i = 0; i < N; i++) {
            System.out.print(array[i]);
            if (i < N-1) System.out.print(", ");
        }
        System.out.println(" ]");
    }
    
    // bubble sort ascending
    public static void sortArray(int[] array, int N) {
        for (int i = 0; i < N - 1; i++) {
            for (int j = 0; j < N - i - 1; j++) {
                if (array[j] > array[j+1]) {
                    int temp = array[j];
                    array[j] = array[j+1];
                    array[j+1] = temp;
                }
            }
        }
    }
    
    // search for element x
    public static boolean findElement(int[] array, int x) {
        for (int i = 0; i < array.length; i++) {
            if (array[i] == x) {
                return true;
            }
        }
        return false;
    }
}
