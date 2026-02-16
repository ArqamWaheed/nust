class Employee {
    String fName;
    String lName;
    double salary;

    Employee(String fn, String ln, double sal) {
        fName = fn;
        lName = ln;
        if(sal > 0)
            salary = sal;
        else
            salary = 0;
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

    void setSalary(double sal) {
        if(sal > 0) 
            salary = sal;
    }
    double getSalary() { 
        return salary; 
    }

    double calcYearlySalary() {
        return salary * 12;
    }
}

public class Task1 {
    public static void main(String args[]) {
        Employee e1 = new Employee("Ali", "Khan", 4500);
        Employee e2 = new Employee("Sara", "Ahmed", 6000);

        System.out.println("First Employee: " + e1.getFName() + " " + e1.getLName());
        System.out.println("Annual Salary: " + e1.calcYearlySalary());
        System.out.println();
        System.out.println("Second Employee: " + e2.getFName() + " " + e2.getLName());
        System.out.println("Annual Salary: " + e2.calcYearlySalary());

        double raise1 = e1.getSalary() * 0.10;
        double raise2 = e2.getSalary() * 0.10;
        e1.setSalary(e1.getSalary() + raise1);
        e2.setSalary(e2.getSalary() + raise2);

        System.out.println();
        System.out.println("After giving 10% raise:");
        System.out.println("First Employee: " + e1.getFName() + " " + e1.getLName());
        System.out.println("Annual Salary: " + e1.calcYearlySalary());
        System.out.println();
        System.out.println("Second Employee: " + e2.getFName() + " " + e2.getLName());
        System.out.println("Annual Salary: " + e2.calcYearlySalary());
    }
}
