import java.util.Scanner;

class HealthProfile {
    String fName, lName, gen;
    int bMonth, bDay, bYear;
    double ht, wt;

    HealthProfile(String fn, String ln, String g, int bm, int bd, int by, double h, double w) {
        fName = fn;
        lName = ln;
        gen = g;
        bMonth = bm;
        bDay = bd;
        bYear = by;
        ht = h;
        wt = w;
    }

    void setFName(String fn) { 
        fName = fn; 
    }
    String getFName() { 
        return fName; 
    }

    void setLName(String ln) { 
        lName = ln; 
    }
    String getLName() { 
        return lName; 
    }

    void setGen(String g) { 
        gen = g; 
    }
    String getGen() { 
        return gen; 
    }

    void setBMonth(int bm) { 
        bMonth = bm; 
    }
    int getBMonth() { 
        return bMonth; 
    }

    void setBDay(int bd) { 
        bDay = bd; 
    }
    int getBDay() { 
        return bDay; 
    }

    void setBYear(int by) { 
        bYear = by; 
    }
    int getBYear() { 
        return bYear; 
    }

    void setHt(double h) { 
        ht = h; 
    }
    double getHt() { 
        return ht; 
    }

    void setWt(double w) { 
        wt = w; 
    }
    double getWt() { 
        return wt; 
    }

    int calcAge() {
        int currYear = 2026;
        int currMonth = 2;
        int currDay = 16;
        int a = currYear - bYear;
        if(currMonth < bMonth)
            a = a - 1;
        else if(currMonth == bMonth && currDay < bDay)
            a = a - 1;
        return a;
    }

    int calcMaxHR() {
        return 220 - calcAge();
    }

    double calcMinTargetHR() {
        return calcMaxHR() * 0.5;
    }

    double calcMaxTargetHR() {
        return calcMaxHR() * 0.85;
    }

    double calcBMI() {
        return (wt * 703) / (ht * ht);
    }
}

public class Task3 {
    public static void main(String args[]) {
        Scanner input = new Scanner(System.in);

        System.out.print("First Name: ");
        String fn = input.next();
        System.out.print("Last Name: ");
        String ln = input.next();
        System.out.print("Gender: ");
        String g = input.next();
        System.out.print("Birth Month: ");
        int bm = input.nextInt();
        System.out.print("Birth Day: ");
        int bd = input.nextInt();
        System.out.print("Birth Year: ");
        int by = input.nextInt();
        System.out.print("Height (inches): ");
        double h = input.nextDouble();
        System.out.print("Weight (pounds): ");
        double w = input.nextDouble();

        HealthProfile p = new HealthProfile(fn, ln, g, bm, bd, by, h, w);

        System.out.println();
        System.out.println("=== Health Profile ===");
        System.out.println("Name: " + p.getFName() + " " + p.getLName());
        System.out.println("Gender: " + p.getGen());
        System.out.println("DOB: " + p.getBMonth() + "/" + p.getBDay() + "/" + p.getBYear());
        System.out.println("Height: " + p.getHt() + " in");
        System.out.println("Weight: " + p.getWt() + " lbs");
        System.out.println("Age: " + p.calcAge());
        System.out.println("BMI: " + p.calcBMI());
        System.out.println("Max Heart Rate: " + p.calcMaxHR());
        System.out.println("Target HR Range: " + p.calcMinTargetHR() + " to " + p.calcMaxTargetHR());

        System.out.println();
        System.out.println("=== BMI Chart ===");
        System.out.println("Underweight = below 18.5");
        System.out.println("Normal = 18.5 to 24.9");
        System.out.println("Overweight = 25 to 29.9");
        System.out.println("Obese = 30 and above");

        input.close();
    }
}
