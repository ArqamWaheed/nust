import java.util.Scanner;

public class Task1Lab9 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        double balance = 2000.0;

        while (true) {
            System.out.println();
            System.out.println("--- ATM ---");
            System.out.println("1) Withdraw");
            System.out.println("2) Deposit");
            System.out.println("3) Check balance");
            System.out.println("4) Exit");
            System.out.print("Choose: ");

            String line = sc.nextLine();
            try {
                int choice = Integer.parseInt(line.trim());
                switch (choice) {
                    case 1:
                        System.out.print("Amount to withdraw: ");
                        String a1 = sc.nextLine();
                        double amt1 = Double.parseDouble(a1.trim());
                        if (amt1 <= 0) {
                            System.out.println("Amount must be positive");
                            break;
                        }
                        if (amt1 > balance) {
                            System.out.println("Insufficient funds");
                            break;
                        }
                        balance -= amt1;
                        System.out.println("Withdrawn " + amt1 + ", balance: " + balance);
                        break;
                    case 2:
                        System.out.print("Amount to deposit: ");
                        String a2 = sc.nextLine();
                        double amt2 = Double.parseDouble(a2.trim());
                        if (amt2 <= 0) {
                            System.out.println("Amount must be positive");
                            break;
                        }
                        balance += amt2;
                        System.out.println("Deposited " + amt2 + ", balance: " + balance);
                        break;
                    case 3:
                        System.out.println("Balance: " + balance);
                        break;
                    case 4:
                        System.out.println("Goodbye");
                        sc.close();
                        return;
                    default:
                        System.out.println("Please choose 1-4");
                }
            } catch (NumberFormatException e) {
                System.out.println("Invalid input, enter a number");
            } catch (Exception e) {
                System.out.println("Error: " + e.getMessage());
            }
        }
    }
}
