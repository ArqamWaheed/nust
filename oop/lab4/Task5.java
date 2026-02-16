import java.util.Scanner;

class QuadraticEquation {
    double a, b, c;

    QuadraticEquation(double a1, double b1, double c1) {
        a = a1;
        b = b1;
        c = c1;
    }

    double getA() { 
        return a; 
    }
    double getB() { 
        return b; 
    }
    double getC() { 
        return c; 
    }

    double calcDiscriminant() {
        return b * b - 4 * a * c;
    }

    double calcRoot1() {
        double disc = calcDiscriminant();
        if(disc < 0)
            return 0;
        else
            return (-b + Math.sqrt(disc)) / (2 * a);
    }

    double calcRoot2() {
        double disc = calcDiscriminant();
        if(disc < 0)
            return 0;
        else
            return (-b - Math.sqrt(disc)) / (2 * a);
    }
}

public class Task5 {
    public static void main(String args[]) {
        Scanner scan = new Scanner(System.in);

        System.out.print("Enter value of a: ");
        double a = scan.nextDouble();
        System.out.print("Enter value of b: ");
        double b = scan.nextDouble();
        System.out.print("Enter value of c: ");
        double c = scan.nextDouble();

        QuadraticEquation eq = new QuadraticEquation(a, b, c);

        double disc = eq.calcDiscriminant();

        System.out.println();
        if(disc > 0) {
            System.out.println("Two roots exist:");
            System.out.println("Root 1 = " + eq.calcRoot1());
            System.out.println("Root 2 = " + eq.calcRoot2());
        }
        else if(disc == 0) {
            System.out.println("One root exists:");
            System.out.println("Root = " + eq.calcRoot1());
        }
        else {
            System.out.println("The equation has no roots.");
        }

        scan.close();
    }
}
