class Applicant {
    String fullName;
    int applicantAge;
    double income;
    int score;

    Applicant(String fullName, int applicantAge, double income, int score) {
        this.fullName = fullName;
        this.applicantAge = applicantAge;
        this.income = income;
        this.score = score;
    }

    void setFullName(String fullName) { 
        this.fullName = fullName; 
    }
    String getFullName() { 
        return fullName; 
    }

    void setApplicantAge(int applicantAge) { 
        this.applicantAge = applicantAge; 
    }
    int getApplicantAge() { 
        return applicantAge; 
    }

    void setIncome(double income) { 
        this.income = income; 
    }
    double getIncome() { 
        return income; 
    }

    void setScore(int score) { 
        this.score = score; 
    }
    int getScore() { 
        return score; 
    }
}

class LoanEvaluator {
    Applicant applicantList[];
    int numApplicants;

    LoanEvaluator(Applicant applicantList[], int numApplicants) {
        this.applicantList = applicantList;
        this.numApplicants = numApplicants;
    }

    boolean isEligible(Applicant app) {
        if(app.getApplicantAge() >= 21 && app.getIncome() >= 50000 && app.getScore() >= 650)
            return true;
        else
            return false;
    }

    String getRejectReason(Applicant app) {
        String msg = "";
        if(app.getApplicantAge() < 21)
            msg = msg + "Age below 21. ";
        if(app.getIncome() < 50000)
            msg = msg + "Income below 50,000. ";
        if(app.getScore() < 650)
            msg = msg + "Credit score below 650. ";
        return msg;
    }

    void showEligibilityReport() {
        int passed = 0;
        int idx = 0;
        while(idx < numApplicants) {
            System.out.print(applicantList[idx].getFullName() + ", " + applicantList[idx].getApplicantAge() 
                             + ", " + applicantList[idx].getIncome() 
                             + ", " + applicantList[idx].getScore());
            if(isEligible(applicantList[idx])) {
                System.out.println(", Eligible");
                passed++;
            }
            else {
                System.out.println(", Not Eligible, " + getRejectReason(applicantList[idx]));
            }
            idx++;
        }
        System.out.println("Total Eligible: " + passed + "/" + numApplicants);
    }
}

public class Task3 {
    public static void main(String args[]) {
        Applicant applicantList[] = new Applicant[5];
        applicantList[0] = new Applicant("Kamran Akmal", 28, 72000, 710);
        applicantList[1] = new Applicant("Ayesha Nawaz", 20, 48000, 690);
        applicantList[2] = new Applicant("Rizwan Sheikh", 35, 55000, 580);
        applicantList[3] = new Applicant("Hina Pervaiz", 24, 62000, 660);
        applicantList[4] = new Applicant("Junaid Iqbal", 19, 40000, 550);

        LoanEvaluator evaluator = new LoanEvaluator(applicantList, 5);
        evaluator.showEligibilityReport();

        System.out.println(applicantList[3].getFullName() + ", Eligible: " + evaluator.isEligible(applicantList[3]));
    }
}
