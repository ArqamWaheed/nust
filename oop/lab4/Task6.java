import java.util.Scanner;

public class Task6 
{
    public static void main(String[] args) 
    {
        Scanner scanner = new Scanner(System.in);
        
        double[] data = new double[10];
        
        System.out.println("Enter 10 numbers:");
        
        int index = 0;
        while(index < 10) {
            System.out.print("Number " + (index+1) + ": ");
            data[index] = scanner.nextDouble();
            index++;
        }
        
        double sum = 0.0;
        for(int i = 0; i < data.length; i++) {
            sum = sum + data[i];
        }
        double average = sum / data.length;
        
        double variance = 0.0;
        for(int i = 0; i < data.length; i++) {
            double difference = data[i] - average;
            variance = variance + (difference * difference);
        }
        
        double standardDeviation = Math.sqrt(variance / (data.length - 1));
        
        System.out.println("Mean: " + String.format("%.2f", average));
        System.out.println("Standard Deviation: " + String.format("%.5f", standardDeviation));
        
        scanner.close();
    }
}
