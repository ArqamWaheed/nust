import java.util.Scanner;

public class Task4 
{
    public static void main(String[] args) 
    {
        Scanner scan = new Scanner(System.in);
        
        System.out.print("Enter loan amount: ");
        double loan = scan.nextDouble();
        
        System.out.print("Enter number of years: ");
        int numYears = scan.nextInt();
        
        if(loan <= 0 || numYears <= 0) {
            System.out.println("Invalid input! Exiting...");
            scan.close();
            return;
        }
        
        System.out.println("Interest Rate    Monthly Payment    Total Payment");
        
        double interestRate = 5.0;
        while(interestRate <= 10.0) {
            double monthlyInterestRate = interestRate / 1200.0;
            int totalMonths = numYears * 12;
            
            double monthlyPay = (loan * monthlyInterestRate) / (1 - Math.pow(1 + monthlyInterestRate, -totalMonths));
            double totalPay = monthlyPay * totalMonths;
            
            System.out.printf("%.2f%%           $%.2f            $%.2f\n", interestRate, monthlyPay, totalPay);
            
            interestRate = interestRate + 0.25;
        }
        
        scan.close();
    }
}
