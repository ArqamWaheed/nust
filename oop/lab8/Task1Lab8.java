class BankAccount {
    String accountNumber;
    String holderName;
    double balance;

    BankAccount(String accountNumber, String holderName, double balance) {
        this.accountNumber = accountNumber;
        this.holderName = holderName;
        this.balance = balance;
    }

    void setAccountNumber(String accountNumber) { 
        this.accountNumber = accountNumber; 
    }
    String getAccountNumber() { 
        return accountNumber; 
    }

    void setHolderName(String holderName) { 
        this.holderName = holderName; 
    }
    String getHolderName() { 
        return holderName; 
    }

    void setBalance(double balance) { 
        this.balance = balance; 
    }
    double getBalance() { 
        return balance; 
    }

    void deposit(double amount) {
        if(amount > 0)
            balance = balance + amount;
    }

    void withdraw(double amount) {
        if(amount > 0 && amount <= balance)
            balance = balance - amount;
    }

    String getAccountType() {
        return "General";
    }
}

class SavingsAccount extends BankAccount {
    double interestRate;

    SavingsAccount(String accountNumber, String holderName, double balance, double interestRate) {
        super(accountNumber, holderName, balance);
        this.interestRate = interestRate;
    }

    void setInterestRate(double interestRate) { 
        this.interestRate = interestRate; 
    }
    double getInterestRate() { 
        return interestRate; 
    }

    double calculateInterest() {
        return balance * interestRate / 100.0;
    }

    void applyInterest() {
        balance = balance + calculateInterest();
    }

    String getAccountType() {
        return "Savings";
    }
}

class CurrentAccount extends BankAccount {
    double overdraftLimit;

    CurrentAccount(String accountNumber, String holderName, double balance, double overdraftLimit) {
        super(accountNumber, holderName, balance);
        this.overdraftLimit = overdraftLimit;
    }

    void setOverdraftLimit(double overdraftLimit) { 
        this.overdraftLimit = overdraftLimit; 
    }
    double getOverdraftLimit() { 
        return overdraftLimit; 
    }

    void withdraw(double amount) {
        if(amount > 0 && amount <= balance + overdraftLimit)
            balance = balance - amount;
    }

    String getAccountType() {
        return "Current";
    }
}

class BankProcessor {
    BankAccount accountList[];
    int totalAccounts;

    BankProcessor(BankAccount accountList[], int totalAccounts) {
        this.accountList = accountList;
        this.totalAccounts = totalAccounts;
    }

    double calcTotalBalance() {
        double sum = 0;
        int idx = 0;
        while(idx < totalAccounts) {
            sum = sum + accountList[idx].getBalance();
            idx++;
        }
        return sum;
    }

    BankAccount findHighestBalanceAfterInterest() {
        BankAccount top = accountList[0];
        double topBal = accountList[0].getBalance();
        if(accountList[0] instanceof SavingsAccount)
            topBal = topBal + ((SavingsAccount) accountList[0]).calculateInterest();

        int idx = 1;
        while(idx < totalAccounts) {
            double bal = accountList[idx].getBalance();
            if(accountList[idx] instanceof SavingsAccount)
                bal = bal + ((SavingsAccount) accountList[idx]).calculateInterest();
            if(bal > topBal) {
                top = accountList[idx];
                topBal = bal;
            }
            idx++;
        }
        return top;
    }

    void showReport() {
        int idx = 0;
        while(idx < totalAccounts) {
            System.out.println(accountList[idx].getAccountNumber() + ", " 
                               + accountList[idx].getHolderName() + ", " 
                               + accountList[idx].getAccountType() + ", Balance: " 
                               + accountList[idx].getBalance());
            idx++;
        }
        System.out.println("Total Bank Balance: " + calcTotalBalance());
        BankAccount top = findHighestBalanceAfterInterest();
        System.out.println("Highest Balance After Interest: " + top.getHolderName() 
                           + ", " + top.getBalance());
    }
}

public class Task1Lab8 {
    public static void main(String args[]) {
        BankAccount accountList[] = new BankAccount[5];
        accountList[0] = new SavingsAccount("SA001", "Ahmed Khan", 50000, 5.0);
        accountList[1] = new CurrentAccount("CA001", "Sara Ali", 30000, 10000);
        accountList[2] = new SavingsAccount("SA002", "Bilal Tariq", 75000, 4.5);
        accountList[3] = new CurrentAccount("CA002", "Hina Rauf", 20000, 5000);
        accountList[4] = new SavingsAccount("SA003", "Usman Javed", 60000, 6.0);

        ((SavingsAccount) accountList[0]).applyInterest();
        ((SavingsAccount) accountList[2]).applyInterest();
        ((SavingsAccount) accountList[4]).applyInterest();

        accountList[1].deposit(5000);
        accountList[3].withdraw(22000);

        BankProcessor processor = new BankProcessor(accountList, 5);
        processor.showReport();

        System.out.println(accountList[2].getHolderName() + ", Balance: " + accountList[2].getBalance());
    }
}
