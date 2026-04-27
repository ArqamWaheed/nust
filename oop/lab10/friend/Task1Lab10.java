
abstract class Consumer {
    private String fullName;
    private int consumerId;
    private int usage;

    Consumer(String fullName, int consumerId, int usage) {
        this.fullName = fullName;
        this.consumerId = consumerId;
        this.usage = usage;
    }

    void setFullName(String fullName) {
        this.fullName = fullName;
    }
    String getFullName() {
        return fullName;
    }

    void setConsumerId(int consumerId) {
        this.consumerId = consumerId;
    }
    int getConsumerId() {
        return consumerId;
    }

    void setUsage(int usage) {
        this.usage = usage;
    }
    int getUsage() {
        return usage;
    }

    abstract String category();
    abstract Invoice calculateBill();
}

class Invoice {
    private int consumedUnits;
    private double amount;
    private String details;

    Invoice(int consumedUnits, double amount, String details) {
        this.consumedUnits = consumedUnits;
        this.amount = amount;
        this.details = details;
    }

    void setConsumedUnits(int consumedUnits) {
        this.consumedUnits = consumedUnits;
    }
    int getConsumedUnits() {
        return consumedUnits;
    }

    void setAmount(double amount) {
        this.amount = amount;
    }
    double getAmount() {
        return amount;
    }

    void setDetails(String details) {
        this.details = details;
    }
    String getDetails() {
        return details;
    }
}

class Household extends Consumer {
    Household(String fullName, int consumerId, int usage) {
        super(fullName, consumerId, usage);
    }

    String category() {
        return "Residential";
    }

    Invoice calculateBill() {
        int u = getUsage();
        String info = "";
        double sub;

        if (u > 100) {
            int extra = u - 100;
            double partOne = 100 * 5;
            double partTwo = extra * 8;
            sub = partOne + partTwo;
            info = info + "First 100 units @ 5/unit   = " + (int) partOne + "\n";
            info = info + "Remaining " + extra + " units @ 8/unit = " + (int) partTwo + "\n";
        } else {
            sub = u * 5;
            info = info + "All " + u + " units @ 5/unit     = " + (int) sub + "\n";
        }

        double discount = sub * 0.10;
        double finalAmount = sub - discount;

        info = info + "Subtotal                   = " + (int) sub + "\n";
        info = info + "Subsidy (-10%)             = -" + (int) discount + "\n";
        info = info + "---------------------------------\n";
        info = info + "Total Bill                 = " + (int) finalAmount + " PKR";

        return new Invoice(u, finalAmount, info);
    }
}

class Shop extends Consumer {
    Shop(String fullName, int consumerId, int usage) {
        super(fullName, consumerId, usage);
    }

    String category() {
        return "Commercial";
    }

    Invoice calculateBill() {
        int u = getUsage();
        double cost = u * 10;
        double svcCharge = 200;
        double beforeTax = cost + svcCharge;
        double taxAmount = beforeTax * 0.05;
        double finalAmount = beforeTax + taxAmount;

        String info = "";
        info = info + "All units @ 10/unit        = " + (int) cost + "\n";
        info = info + "Service Charges            = " + (int) svcCharge + "\n";
        info = info + "Tax (5%)                   = " + (int) taxAmount + "\n";
        info = info + "---------------------------------\n";
        info = info + "Total Bill                 = " + (int) finalAmount + " PKR";

        return new Invoice(u, finalAmount, info);
    }
}

class Factory extends Consumer {
    Factory(String fullName, int consumerId, int usage) {
        super(fullName, consumerId, usage);
    }

    String category() {
        return "Industrial";
    }

    Invoice calculateBill() {
        int u = getUsage();
        double cost = u * 12;
        double peakSurcharge = 300;
        double beforeTax = cost + peakSurcharge;
        double taxAmount = beforeTax * 0.10;
        double finalAmount = beforeTax + taxAmount;

        String info = "";
        info = info + "All units @ 12/unit        = " + (int) cost + "\n";
        info = info + "Peak Hour Charges          = " + (int) peakSurcharge + "\n";
        info = info + "Tax (10%)                  = " + (int) taxAmount + "\n";
        info = info + "---------------------------------\n";
        info = info + "Total Bill                 = " + (int) finalAmount + " PKR";

        return new Invoice(u, finalAmount, info);
    }
}

public class Task1Lab10 {
    public static void main(String args[]) {
        Consumer list[] = new Consumer[3];
        list[0] = new Household("Ali Khan", 101, 120);
        list[1] = new Shop("Sara Ahmed", 102, 120);
        list[2] = new Factory("Usman Tariq", 103, 120);

        System.out.println("========== ELECTRICITY BILLING SYSTEM ==========");

        int idx = 0;
        while (idx < list.length) {
            Consumer con = list[idx];
            Invoice inv = con.calculateBill();

            System.out.println("Customer ID: " + con.getConsumerId());
            System.out.println("Name: " + con.getFullName());
            System.out.println("Type: " + con.category());
            System.out.println("Units Consumed: " + con.getUsage());
            System.out.println();
            System.out.println("--- Bill Breakdown ---");
            System.out.println(inv.getDetails());
            System.out.println();
            System.out.println("-----------------------------------------------");
            System.out.println();
            idx++;
        }

        System.out.println("===============================================");
        System.out.println("Summary:");
        System.out.println("Total Customers Processed: " + list.length);
    }
}
