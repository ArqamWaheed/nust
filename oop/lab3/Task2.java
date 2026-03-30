import java.util.Scanner;

// task 2 - count how many nums are >= 10
public class Task2 {
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int[] numbers = new int[10];
        
        System.out.println("Enter 10 integers:");
        System.out.println("------------------");
        
        for (int i = 0; i < 10; i++) {
            System.out.print("Enter integer #" + (i+1) + ": ");
            numbers[i] = scanner.nextInt();
        }
        
        int count = countGreaterOrEqual(numbers, 10);
        
        System.out.println();
        System.out.println("================================");
        System.out.println("Total integers >= 10: " + count);
        System.out.println("================================");
        
        scanner.close();
    }
    
    // counts elements >= threshold
    public static int countGreaterOrEqual(int[] arr, int threshold) {
        int count = 0;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] >= threshold) {
                count++;
            }
        }
        return count;
    }
}
