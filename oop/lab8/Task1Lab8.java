class BankAccount {
    String accNo;
    String name;
    double bal;

    BankAccount(String accNo, String name, double bal) {
        this.accNo = accNo;
        this.name = name;
        this.bal = bal;
    }

    void setAccNo(String accNo) { 
        this.accNo = accNo; 
    }
    String getAccNo() { 
        return accNo; 
    }

    void setName(String name) { 
        this.name = name; 
    }
    String getName() { 
        return name; 
    }

    void setBal(double bal) { 
        this.bal = bal; 
    }
    double getBal() { 
        return bal; 
    }

    String type() {
        return "General";
    }

    void deposit(double amt) {
        if(amt > 0)
            bal = bal + amt;
    }

    void withdraw(double amt) {
        if(amt > 0 && amt <= bal)
            bal = bal - amt;
    }
}

class SavingsAccount extends BankAccount {
    double rate;

    SavingsAccount(String accNo, String name, double bal, double rate) {
        super(accNo, name, bal);
        this.rate = rate;
    }

    void setRate(double rate) { 
        this.rate = rate; 
    }
    double getRate() { 
        return rate; 
    }

    String type() {
        return "Savings";
    }

    double calcInterest() {
        return bal * rate / 100.0;
    }

    void addInterest() {
        bal = bal + calcInterest();
    }
}

class CurrentAccount extends BankAccount {
    double limit;

    CurrentAccount(String accNo, String name, double bal, double limit) {
        super(accNo, name, bal);
        this.limit = limit;
    }

    void setLimit(double limit) { 
        this.limit = limit; 
    }
    double getLimit() { 
        return limit; 
    }

    String type() {
        return "Current";
    }

    void withdraw(double amt) {
        if(amt > 0 && amt <= bal + limit)
            bal = bal - amt;
    }
}

class BankManager {
    BankAccount accounts[];
    int count;

    BankManager(BankAccount accounts[], int count) {
        this.accounts = accounts;
        this.count = count;
    }

    void printAll() {
        int i = 0;
        while(i < count) {
            System.out.println(accounts[i].getAccNo() + ", " 
                               + accounts[i].getName() + ", " 
                               + accounts[i].type() + ", Bal: " 
                               + accounts[i].getBal());
            i++;
        }
    }

    double totalBalance() {
        double total = 0;
        int i = 0;
        while(i < count) {
            total = total + accounts[i].getBal();
            i++;
        }
        return total;
    }

    BankAccount highestAfterInterest() {
        BankAccount best = accounts[0];
        double bestBal = accounts[0].getBal();
        if(accounts[0] instanceof SavingsAccount)
            bestBal = bestBal + ((SavingsAccount) accounts[0]).calcInterest();

        int i = 1;
        while(i < count) {
            double b = accounts[i].getBal();
            if(accounts[i] instanceof SavingsAccount)
                b = b + ((SavingsAccount) accounts[i]).calcInterest();
            if(b > bestBal) {
                best = accounts[i];
                bestBal = b;
            }
            i++;
        }
        return best;
    }

    void report() {
        printAll();
        System.out.println("Total Balance: " + totalBalance());
        BankAccount best = highestAfterInterest();
        System.out.println("Highest After Interest: " + best.getName() 
                           + ", Bal: " + best.getBal());
    }
}

public class Task1Lab8 {
    public static void main(String args[]) {
        BankAccount accounts[] = new BankAccount[5];
        accounts[0] = new CurrentAccount("C101", "Waseem Akram", 45000, 8000);
        accounts[1] = new SavingsAccount("S101", "Noman Sheikh", 62000, 4.0);
        accounts[2] = new SavingsAccount("S102", "Ayesha Baig", 80000, 5.5);
        accounts[3] = new CurrentAccount("C102", "Rizwan Haider", 15000, 6000);
        accounts[4] = new SavingsAccount("S103", "Tahira Begum", 55000, 3.5);

        accounts[0].deposit(10000);
        ((SavingsAccount) accounts[1]).addInterest();
        ((SavingsAccount) accounts[2]).addInterest();
        accounts[3].withdraw(18000);
        ((SavingsAccount) accounts[4]).addInterest();

        BankManager mgr = new BankManager(accounts, 5);
        mgr.report();

        System.out.println(accounts[1].getName() + ", Bal: " + accounts[1].getBal());
    }
}
