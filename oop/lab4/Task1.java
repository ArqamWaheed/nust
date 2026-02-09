import java.util.Scanner;

// task 1 - position equation in physics
public class Task1 
{
    public static void main(String[] args) 
    {
        Scanner input = new Scanner(System.in);
        
        System.out.print("Enter initial position (s0): ");
        double initialPosition = input.nextDouble();
        
        System.out.print("Enter initial velocity (v0): ");
        double initialVelocity = input.nextDouble();
        
        System.out.print("Enter acceleration (a): ");
        double acceleration = input.nextDouble();
        
        System.out.print("Enter time (t): ");
        double time = input.nextDouble();
        
        double position = initialPosition + initialVelocity * time + (acceleration * time * time) / 2;
        
        System.out.println("Position at time " + time + ": " + position);
        
        input.close();
    }
}
