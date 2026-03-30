class Family {
    String familyHead;
    int numMembers;
    int severity;
    int daysWithoutAid;

    Family(String familyHead, int numMembers, int severity, int daysWithoutAid) {
        this.familyHead = familyHead;
        this.numMembers = numMembers;
        this.severity = severity;
        this.daysWithoutAid = daysWithoutAid;
    }

    void setFamilyHead(String familyHead) { 
        this.familyHead = familyHead; 
    }
    String getFamilyHead() { 
        return familyHead; 
    }

    void setNumMembers(int numMembers) { 
        this.numMembers = numMembers; 
    }
    int getNumMembers() { 
        return numMembers; 
    }

    void setSeverity(int severity) { 
        this.severity = severity; 
    }
    int getSeverity() { 
        return severity; 
    }

    void setDaysWithoutAid(int daysWithoutAid) { 
        this.daysWithoutAid = daysWithoutAid; 
    }
    int getDaysWithoutAid() { 
        return daysWithoutAid; 
    }

    int calcRequiredPackages() {
        int packs = (int) Math.ceil(numMembers / 2.0);
        if(severity == 3)
            packs = packs + 2;
        return packs;
    }

    String getSeverityText() {
        if(severity == 1)
            return "Low";
        else if(severity == 2)
            return "Medium";
        else
            return "Critical";
    }
}

class ReliefAllocator {
    Family familyList[];
    int totalFamilies;

    ReliefAllocator(Family familyList[], int totalFamilies) {
        this.familyList = familyList;
        this.totalFamilies = totalFamilies;
    }

    int calcTotalPackages() {
        int sum = 0;
        int idx = 0;
        while(idx < totalFamilies) {
            sum = sum + familyList[idx].calcRequiredPackages();
            idx++;
        }
        return sum;
    }

    Family findTopPriority() {
        Family top = familyList[0];
        int idx = 1;
        while(idx < totalFamilies) {
            if(familyList[idx].getSeverity() > top.getSeverity())
                top = familyList[idx];
            else if(familyList[idx].getSeverity() == top.getSeverity() 
                     && familyList[idx].getDaysWithoutAid() > top.getDaysWithoutAid())
                top = familyList[idx];
            idx++;
        }
        return top;
    }

    void showReport() {
        int idx = 0;
        while(idx < totalFamilies) {
            System.out.println(familyList[idx].getFamilyHead() + ", " + familyList[idx].getNumMembers() 
                               + ", " + familyList[idx].getSeverityText() + ", " 
                               + familyList[idx].getDaysWithoutAid() + " days, " 
                               + familyList[idx].calcRequiredPackages() + " packages");
            idx++;
        }
        System.out.println("Total Packages: " + calcTotalPackages());
        Family top = findTopPriority();
        System.out.println("Priority: " + top.getFamilyHead() + ", " 
                           + top.getSeverityText() + ", " + top.getDaysWithoutAid() + " days");
    }
}

public class Task1 {
    public static void main(String args[]) {
        Family familyList[] = new Family[5];
        familyList[0] = new Family("Tariq Mehmood", 5, 2, 8);
        familyList[1] = new Family("Imran Siddiqui", 7, 3, 12);
        familyList[2] = new Family("Naveed Akhtar", 3, 1, 2);
        familyList[3] = new Family("Salman Javed", 4, 3, 18);
        familyList[4] = new Family("Waqas Younis", 6, 2, 5);

        ReliefAllocator allocator = new ReliefAllocator(familyList, 5);
        allocator.showReport();

        System.out.println(familyList[4].getFamilyHead() + ", " + familyList[4].calcRequiredPackages() + " packages");
    }
}
