class Patient {
    String pid;
    String name;
    int age;
    double temp;
    int pulse;
    int severity;

    Patient(String pid, String name, int age, double temp, int pulse, int severity) {
        this.pid = pid;
        this.name = name;
        this.age = age;
        this.temp = temp;
        this.pulse = pulse;
        this.severity = severity;
    }

    void setPid(String pid) { 
        this.pid = pid; 
    }
    String getPid() { 
        return pid; 
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

    void setTemp(double temp) { 
        this.temp = temp; 
    }
    double getTemp() { 
        return temp; 
    }

    void setPulse(int pulse) { 
        this.pulse = pulse; 
    }
    int getPulse() { 
        return pulse; 
    }

    void setSeverity(int severity) { 
        this.severity = severity; 
    }
    int getSeverity() { 
        return severity; 
    }

    String checkHealth() {
        if(severity >= 3)
            return "Critical";
        else if(severity == 2)
            return "Moderate";
        return "Stable";
    }

    String kind() {
        return "General";
    }

    int monitorGap() {
        return 60;
    }
}

class HeartPatient extends Patient {
    int sysBP;
    int diaBP;

    HeartPatient(String pid, String name, int age, double temp, int pulse, 
                 int severity, int sysBP, int diaBP) {
        super(pid, name, age, temp, pulse, severity);
        this.sysBP = sysBP;
        this.diaBP = diaBP;
    }

    void setSysBP(int sysBP) { 
        this.sysBP = sysBP; 
    }
    int getSysBP() { 
        return sysBP; 
    }

    void setDiaBP(int diaBP) { 
        this.diaBP = diaBP; 
    }
    int getDiaBP() { 
        return diaBP; 
    }

    String kind() {
        return "Heart";
    }

    String checkHealth() {
        if(pulse > 120 || sysBP > 180)
            return "Critical";
        else if(pulse > 100 || sysBP > 140)
            return "Moderate";
        return "Stable";
    }

    int monitorGap() {
        if(severity >= 3)
            return 5;
        return 15;
    }
}

class InfectionPatient extends Patient {
    String disease;
    boolean quarantined;

    InfectionPatient(String pid, String name, int age, double temp, int pulse, 
                     int severity, String disease, boolean quarantined) {
        super(pid, name, age, temp, pulse, severity);
        this.disease = disease;
        this.quarantined = quarantined;
    }

    void setDisease(String disease) { 
        this.disease = disease; 
    }
    String getDisease() { 
        return disease; 
    }

    void setQuarantined(boolean quarantined) { 
        this.quarantined = quarantined; 
    }
    boolean getQuarantined() { 
        return quarantined; 
    }

    String kind() {
        return "Infection";
    }

    String checkHealth() {
        if(temp > 103.0 || severity >= 3)
            return "Critical";
        else if(temp > 100.0 || severity == 2)
            return "Moderate";
        return "Stable";
    }

    int monitorGap() {
        if(quarantined)
            return 10;
        return 30;
    }
}

class PatientTracker {
    Patient list[];
    int total;

    PatientTracker(Patient list[], int total) {
        this.list = list;
        this.total = total;
    }

    int criticalCount() {
        int c = 0;
        int i = 0;
        while(i < total) {
            if(list[i].checkHealth().equals("Critical"))
                c++;
            i++;
        }
        return c;
    }

    void listCritical() {
        System.out.println("--- Critical ---");
        int i = 0;
        while(i < total) {
            if(list[i].checkHealth().equals("Critical"))
                System.out.println(list[i].getPid() + ", " + list[i].getName() 
                                   + ", " + list[i].kind());
            i++;
        }
    }

    void checkOne(int idx) {
        Patient p = list[idx];
        System.out.println("Patient: " + p.getName() + ", Kind: " + p.kind() 
                           + ", Health: " + p.checkHealth() 
                           + ", Every " + p.monitorGap() + " mins");
    }

    void report() {
        int i = 0;
        while(i < total) {
            System.out.println(list[i].getPid() + ", " + list[i].getName() 
                               + ", " + list[i].kind() + ", " + list[i].checkHealth() 
                               + ", Every " + list[i].monitorGap() + " mins");
            i++;
        }
        System.out.println("Critical Count: " + criticalCount());
        listCritical();
    }
}

public class Task2Lab8 {
    public static void main(String args[]) {
        Patient list[] = new Patient[5];
        list[0] = new InfectionPatient("H01", "Asad Rafi", 28, 104.5, 88, 3, "Dengue", true);
        list[1] = new HeartPatient("H02", "Sajid Awan", 62, 98.1, 125, 3, 190, 105);
        list[2] = new InfectionPatient("H03", "Maryam Latif", 35, 99.2, 76, 1, "Flu", false);
        list[3] = new HeartPatient("H04", "Zubair Anwar", 50, 97.9, 92, 2, 135, 88);
        list[4] = new InfectionPatient("H05", "Rabia Naz", 40, 101.3, 82, 2, "Malaria", true);

        PatientTracker tracker = new PatientTracker(list, 5);
        tracker.report();

        System.out.println();
        tracker.checkOne(2);
    }
}
