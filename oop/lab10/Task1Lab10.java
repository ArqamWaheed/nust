import java.util.ArrayList;

class Bill {
    private int units;
    private double totalCost;
    private String breakdown;

    Bill(int units, double totalCost, String breakdown) {
        this.units = units;
        this.totalCost = totalCost;
        this.breakdown = breakdown;
    }

    void setUnits(int units) { 
        this.units = units; 
    }
    int getUnits() { 
        return units; 
    }

    void setTotalCost(double totalCost) { 
        this.totalCost = totalCost; 
    }
    double getTotalCost() { 
        return totalCost; 
    }

    void setBreakdown(String breakdown) { 
        this.breakdown = breakdown; 
    }
    String getBreakdown() { 
        return breakdown; 
    }
}

abstract class Customer {
    private int id;
    private String name;
    private int unitsConsumed;

    Customer(int id, String name, int unitsConsumed) {
        this.id = id;
        this.name = name;
        this.unitsConsumed = unitsConsumed;
    }

    void setId(int id) { 
        this.id = id; 
    }
    int getId() { 
        return id; 
    }

    void setName(String name) { 
        this.name = name; 
    }
    String getName() { 
        return name; 
    }

    void setUnitsConsumed(int unitsConsumed) { 
        this.unitsConsumed = unitsConsumed; 
    }
    int getUnitsConsumed() { 
        return unitsConsumed; 
    }

    abstract String getType();
    abstract Bill generateBill();
}

class ResidentialCustomer extends Customer {
    ResidentialCustomer(int id, String name, int unitsConsumed) {
        super(id, name, unitsConsumed);
    }

    String getType() {
        return "Residential";
    }

    Bill generateBill() {
        int units = getUnitsConsumed();
        double subtotal = 0;
        String breakdown = "";

        if (units <= 100) {
            subtotal = units * 5;
            breakdown = "All " + units + " units @ 5/unit     = " + (int) subtotal + "\n";
        } else {
            double first = 100 * 5;
            int remaining = units - 100;
            double rest = remaining * 8;
            subtotal = first + rest;
            breakdown = "First 100 units @ 5/unit   = " + (int) first + "\n";
            breakdown += "Remaining " + remaining + " units @ 8/unit = " + (int) rest + "\n";
        }

        double subsidy = subtotal * 0.10;
        double total = subtotal - subsidy;

        breakdown += "Subtotal                   = " + (int) subtotal + "\n";
        breakdown += "Subsidy (-10%)             = -" + (int) subsidy + "\n";
        breakdown += "---------------------------------\n";
        breakdown += "Total Bill                 = " + (int) total + " PKR";

        return new Bill(units, total, breakdown);
    }
}

class CommercialCustomer extends Customer {
    CommercialCustomer(int id, String name, int unitsConsumed) {
        super(id, name, unitsConsumed);
    }

    String getType() {
        return "Commercial";
    }

    Bill generateBill() {
        int units = getUnitsConsumed();
        double unitCost = units * 10;
        double serviceCharges = 200;
        double subtotal = unitCost + serviceCharges;
        double tax = subtotal * 0.05;
        double total = subtotal + tax;

        String breakdown = "";
        breakdown += "All units @ 10/unit        = " + (int) unitCost + "\n";
        breakdown += "Service Charges            = " + (int) serviceCharges + "\n";
        breakdown += "Tax (5%)                   = " + (int) tax + "\n";
        breakdown += "---------------------------------\n";
        breakdown += "Total Bill                 = " + (int) total + " PKR";

        return new Bill(units, total, breakdown);
    }
}

class IndustrialCustomer extends Customer {
    IndustrialCustomer(int id, String name, int unitsConsumed) {
        super(id, name, unitsConsumed);
    }

    String getType() {
        return "Industrial";
    }

    Bill generateBill() {
        int units = getUnitsConsumed();
        double unitCost = units * 12;
        double peakCharges = 300;
        double subtotal = unitCost + peakCharges;
        double tax = subtotal * 0.10;
        double total = subtotal + tax;

        String breakdown = "";
        breakdown += "All units @ 12/unit        = " + (int) unitCost + "\n";
        breakdown += "Peak Hour Charges          = " + (int) peakCharges + "\n";
        breakdown += "Tax (10%)                  = " + (int) tax + "\n";
        breakdown += "---------------------------------\n";
        breakdown += "Total Bill                 = " + (int) total + " PKR";

        return new Bill(units, total, breakdown);
    }
}

public class Task1Lab10 {
    public static void main(String args[]) {
        ArrayList<Customer> customers = new ArrayList<>();
        customers.add(new ResidentialCustomer(101, "Ali Khan", 120));
        customers.add(new CommercialCustomer(102, "Sara Ahmed", 120));
        customers.add(new IndustrialCustomer(103, "Usman Tariq", 120));

        System.out.println("========== ELECTRICITY BILLING SYSTEM ==========");

        int i = 0;
        while (i < customers.size()) {
            Customer c = customers.get(i);
            Bill bill = c.generateBill();

            System.out.println("Customer ID: " + c.getId());
            System.out.println("Name: " + c.getName());
            System.out.println("Type: " + c.getType());
            System.out.println("Units Consumed: " + c.getUnitsConsumed());
            System.out.println();
            System.out.println("--- Bill Breakdown ---");
            System.out.println(bill.getBreakdown());
            System.out.println();
            System.out.println("-----------------------------------------------");
            System.out.println();
            i++;
        }

        System.out.println("===============================================");
        System.out.println("Summary:");
        System.out.println("Total Customers Processed: " + customers.size());
    }
}
