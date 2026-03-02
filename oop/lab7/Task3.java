class Applicant {
    String name;
    int age;
    double monthlyIncome;
    int creditScore;

    Applicant(String name, int age, double monthlyIncome, int creditScore) {
        this.name = name;
        this.age = age;
        this.monthlyIncome = monthlyIncome;
        this.creditScore = creditScore;
    }

    void setName(String name) { 
        this.name = name; 
    }
    String getName() { 
        return name; 
    }

    void setAge(int age) { 
        this.age = age; 
    }
    int getAge() { 
        return age; 
    }

    void setMonthlyIncome(double monthlyIncome) { 
        this.monthlyIncome = monthlyIncome; 
    }
    double getMonthlyIncome() { 
        return monthlyIncome; 
    }

    void setCreditScore(int creditScore) { 
        this.creditScore = creditScore; 
    }
    int getCreditScore() { 
        return creditScore; 
    }
}

class LoanEvaluator {
    Applicant applicants[];
    int applicantCount;

    LoanEvaluator(Applicant applicants[], int applicantCount) {
        this.applicants = applicants;
        this.applicantCount = applicantCount;
    }

    boolean checkEligibility(Applicant applicant) {
        if(applicant.getAge() >= 21 && applicant.getMonthlyIncome() >= 50000 && applicant.getCreditScore() >= 650)
            return true;
        else
            return false;
    }

    String getRejectionReason(Applicant applicant) {
        String reason = "";
        if(applicant.getAge() < 21)
            reason = reason + "Age below 21. ";
        if(applicant.getMonthlyIncome() < 50000)
            reason = reason + "Income below 50,000. ";
        if(applicant.getCreditScore() < 650)
            reason = reason + "Credit score below 650. ";
        return reason;
    }

    void printEligibilityReport() {
        System.out.println("========================================");
        System.out.println("   BANK LOAN ELIGIBILITY REPORT");
        System.out.println("========================================");
        int eligible = 0;
        int i = 0;
        while(i < applicantCount) {
            System.out.println("Applicant: " + applicants[i].getName());
            System.out.println("Age: " + applicants[i].getAge());
            System.out.println("Monthly Income: Rs. " + applicants[i].getMonthlyIncome());
            System.out.println("Credit Score: " + applicants[i].getCreditScore());
            if(checkEligibility(applicants[i])) {
                System.out.println("Status: ELIGIBLE");
                eligible++;
            }
            else {
                System.out.println("Status: NOT ELIGIBLE");
                System.out.println("Reason: " + getRejectionReason(applicants[i]));
            }
            System.out.println("----------------------------------------");
            i++;
        }
        System.out.println("Total Eligible: " + eligible + " out of " + applicantCount);
        System.out.println("========================================");
    }
}

public class Task3 {
    public static void main(String args[]) {
        Applicant applicants[] = new Applicant[4];
        applicants[0] = new Applicant("Ahmed Ali", 25, 60000, 700);
        applicants[1] = new Applicant("Sara Khan", 19, 55000, 680);
        applicants[2] = new Applicant("Usman Tariq", 30, 45000, 720);
        applicants[3] = new Applicant("Nadia Shah", 22, 75000, 600);

        LoanEvaluator evaluator = new LoanEvaluator(applicants, 4);
        evaluator.printEligibilityReport();

        System.out.println();
        System.out.println("Checking individual applicant:");
        System.out.println("Applicant: " + applicants[0].getName());
        System.out.println("Eligible: " + evaluator.checkEligibility(applicants[0]));
    }
}
