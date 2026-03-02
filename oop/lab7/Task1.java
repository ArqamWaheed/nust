class Family {
    String headName;
    int memberCount;
    int severityLevel;
    int daysSinceLastAid;

    Family(String headName, int memberCount, int severityLevel, int daysSinceLastAid) {
        this.headName = headName;
        this.memberCount = memberCount;
        this.severityLevel = severityLevel;
        this.daysSinceLastAid = daysSinceLastAid;
    }

    void setHeadName(String headName) { 
        this.headName = headName; 
    }
    String getHeadName() { 
        return headName; 
    }

    void setMemberCount(int memberCount) { 
        this.memberCount = memberCount; 
    }
    int getMemberCount() { 
        return memberCount; 
    }

    void setSeverityLevel(int severityLevel) { 
        this.severityLevel = severityLevel; 
    }
    int getSeverityLevel() { 
        return severityLevel; 
    }

    void setDaysSinceLastAid(int daysSinceLastAid) { 
        this.daysSinceLastAid = daysSinceLastAid; 
    }
    int getDaysSinceLastAid() { 
        return daysSinceLastAid; 
    }

    int calcPackagesRequired() {
        int packages = (int) Math.ceil(memberCount / 2.0);
        if(severityLevel == 3)
            packages = packages + 2;
        return packages;
    }

    String getSeverityLabel() {
        if(severityLevel == 1)
            return "Low";
        else if(severityLevel == 2)
            return "Medium";
        else
            return "Critical";
    }
}

class ReliefAllocator {
    Family families[];
    int familyCount;

    ReliefAllocator(Family families[], int familyCount) {
        this.families = families;
        this.familyCount = familyCount;
    }

    int calcTotalPackages() {
        int total = 0;
        int i = 0;
        while(i < familyCount) {
            total = total + families[i].calcPackagesRequired();
            i++;
        }
        return total;
    }

    Family findImmediatePriority() {
        Family priority = families[0];
        int i = 1;
        while(i < familyCount) {
            if(families[i].getSeverityLevel() > priority.getSeverityLevel())
                priority = families[i];
            else if(families[i].getSeverityLevel() == priority.getSeverityLevel() 
                     && families[i].getDaysSinceLastAid() > priority.getDaysSinceLastAid())
                priority = families[i];
            i++;
        }
        return priority;
    }

    void printAllocationReport() {
        System.out.println("========================================");
        System.out.println("   DISASTER RELIEF ALLOCATION REPORT");
        System.out.println("========================================");
        int i = 0;
        while(i < familyCount) {
            System.out.println("Family Head: " + families[i].getHeadName());
            System.out.println("Members: " + families[i].getMemberCount());
            System.out.println("Severity: " + families[i].getSeverityLabel());
            System.out.println("Days Since Last Aid: " + families[i].getDaysSinceLastAid());
            System.out.println("Packages Required: " + families[i].calcPackagesRequired());
            System.out.println("----------------------------------------");
            i++;
        }
        System.out.println("Total Packages Required: " + calcTotalPackages());
        Family priority = findImmediatePriority();
        System.out.println("Immediate Priority: " + priority.getHeadName() 
                           + " (Severity: " + priority.getSeverityLabel() 
                           + ", Days: " + priority.getDaysSinceLastAid() + ")");
        System.out.println("========================================");
    }
}

public class Task1 {
    public static void main(String args[]) {
        Family families[] = new Family[4];
        families[0] = new Family("Ahmed Khan", 6, 3, 10);
        families[1] = new Family("Bilal Shah", 4, 1, 3);
        families[2] = new Family("Kashif Ali", 8, 2, 7);
        families[3] = new Family("Danish Raza", 3, 3, 15);

        ReliefAllocator allocator = new ReliefAllocator(families, 4);
        allocator.printAllocationReport();

        System.out.println();
        System.out.println("Analyzing single family:");
        System.out.println("Family Head: " + families[2].getHeadName());
        System.out.println("Packages Required: " + families[2].calcPackagesRequired());
    }
}
