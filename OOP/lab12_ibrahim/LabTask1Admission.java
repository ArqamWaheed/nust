import java.util.Scanner;

class InvalidAgeException extends Exception {
    public InvalidAgeException(String msg) { super(msg); }
}

class InvalidMarksException extends Exception {
    public InvalidMarksException(String msg) { super(msg); }
}

public class LabTask1Admission {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        try {
            System.out.print("Enter student name: ");
            String name = sc.nextLine();

            System.out.print("Enter age: ");
            int age = sc.nextInt();
            if (age < 18) {
                throw new InvalidAgeException("Age " + age + " is below 18, not eligible for admission");
            }

            System.out.print("Enter marks (0 to 100): ");
            double marks = sc.nextDouble();
            if (marks < 0 || marks > 100) {
                throw new InvalidMarksException("Marks " + marks + " are outside the valid range 0 to 100");
            }

            System.out.println("Admission accepted for " + name);
            System.out.println("Age: " + age + ", Marks: " + marks);
        } catch (InvalidAgeException e) {
            System.out.println("InvalidAgeException: " + e.getMessage());
        } catch (InvalidMarksException e) {
            System.out.println("InvalidMarksException: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("Invalid input type. Please enter values in the correct format.");
        } finally {
            sc.close();
        }
    }
}
