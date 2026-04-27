import java.util.Scanner;

public class Task2Lab9 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        try {
            System.out.print("Student name: ");
            String name = sc.nextLine();

            System.out.print("Number of subjects: ");
            String s = sc.nextLine();
            int n = Integer.parseInt(s.trim());
            if (n <= 0) {
                System.out.println("Number of subjects must be greater than zero");
                return;
            }

            double total = 0.0;
            int i = 0;
            while (i < n) {
                System.out.print("Marks for subject " + (i + 1) + ": ");
                String mstr = sc.nextLine();
                try {
                    double mark = Double.parseDouble(mstr.trim());
                    if (mark < 0 || mark > 100) {
                        System.out.println("Marks must be between 0 and 100");
                        continue;
                    }
                    total += mark;
                    i++;
                } catch (NumberFormatException e) {
                    System.out.println("Invalid input, please enter a number");
                }
            }

            double average = total / n;
            String grade;
            if (average >= 80) grade = "A";
            else if (average >= 70) grade = "B";
            else if (average >= 60) grade = "C";
            else if (average >= 50) grade = "D";
            else grade = "F";

            System.out.println();
            System.out.println("Name: " + name);
            System.out.println("Total: " + total);
            System.out.printf("Average: %.2f%n", average);
            System.out.println("Grade: " + grade);
        } catch (NumberFormatException e) {
            System.out.println("Invalid input, please enter a valid number");
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        } finally {
            sc.close();
        }
    }
}
