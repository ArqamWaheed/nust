class Patient {
    String patientId;
    String name;
    int age;
    int heartRate;
    double temperature;
    int severityLevel;

    Patient(String patientId, String name, int age, int heartRate, double temperature, int severityLevel) {
        this.patientId = patientId;
        this.name = name;
        this.age = age;
        this.heartRate = heartRate;
        this.temperature = temperature;
        this.severityLevel = severityLevel;
    }

    void setPatientId(String patientId) { 
        this.patientId = patientId; 
    }
    String getPatientId() { 
        return patientId; 
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

    void setHeartRate(int heartRate) { 
        this.heartRate = heartRate; 
    }
    int getHeartRate() { 
        return heartRate; 
    }

    void setTemperature(double temperature) { 
        this.temperature = temperature; 
    }
    double getTemperature() { 
        return temperature; 
    }

    void setSeverityLevel(int severityLevel) { 
        this.severityLevel = severityLevel; 
    }
    int getSeverityLevel() { 
        return severityLevel; 
    }

    String evaluateHealth() {
        if(severityLevel >= 3)
            return "Critical";
        else if(severityLevel == 2)
            return "Moderate";
        else
            return "Stable";
    }

    int getMonitoringFrequency() {
        return 60;
    }

    String getPatientType() {
        return "General";
    }
}

class CardiacPatient extends Patient {
    int bloodPressureSystolic;
    int bloodPressureDiastolic;

    CardiacPatient(String patientId, String name, int age, int heartRate, double temperature, 
                   int severityLevel, int bloodPressureSystolic, int bloodPressureDiastolic) {
        super(patientId, name, age, heartRate, temperature, severityLevel);
        this.bloodPressureSystolic = bloodPressureSystolic;
        this.bloodPressureDiastolic = bloodPressureDiastolic;
    }

    void setBloodPressureSystolic(int bloodPressureSystolic) { 
        this.bloodPressureSystolic = bloodPressureSystolic; 
    }
    int getBloodPressureSystolic() { 
        return bloodPressureSystolic; 
    }

    void setBloodPressureDiastolic(int bloodPressureDiastolic) { 
        this.bloodPressureDiastolic = bloodPressureDiastolic; 
    }
    int getBloodPressureDiastolic() { 
        return bloodPressureDiastolic; 
    }

    String evaluateHealth() {
        if(heartRate > 120 || bloodPressureSystolic > 180)
            return "Critical";
        else if(heartRate > 100 || bloodPressureSystolic > 140)
            return "Moderate";
        else
            return "Stable";
    }

    int getMonitoringFrequency() {
        if(severityLevel >= 3)
            return 5;
        else
            return 15;
    }

    String getPatientType() {
        return "Cardiac";
    }
}

class InfectiousPatient extends Patient {
    String infectionType;
    boolean isQuarantined;

    InfectiousPatient(String patientId, String name, int age, int heartRate, double temperature, 
                      int severityLevel, String infectionType, boolean isQuarantined) {
        super(patientId, name, age, heartRate, temperature, severityLevel);
        this.infectionType = infectionType;
        this.isQuarantined = isQuarantined;
    }

    void setInfectionType(String infectionType) { 
        this.infectionType = infectionType; 
    }
    String getInfectionType() { 
        return infectionType; 
    }

    void setIsQuarantined(boolean isQuarantined) { 
        this.isQuarantined = isQuarantined; 
    }
    boolean getIsQuarantined() { 
        return isQuarantined; 
    }

    String evaluateHealth() {
        if(temperature > 103.0 || severityLevel >= 3)
            return "Critical";
        else if(temperature > 100.0 || severityLevel == 2)
            return "Moderate";
        else
            return "Stable";
    }

    int getMonitoringFrequency() {
        if(isQuarantined)
            return 10;
        else
            return 30;
    }

    String getPatientType() {
        return "Infectious";
    }
}

class HospitalMonitor {
    Patient patientList[];
    int totalPatients;

    HospitalMonitor(Patient patientList[], int totalPatients) {
        this.patientList = patientList;
        this.totalPatients = totalPatients;
    }

    int countCritical() {
        int count = 0;
        int idx = 0;
        while(idx < totalPatients) {
            if(patientList[idx].evaluateHealth().equals("Critical"))
                count++;
            idx++;
        }
        return count;
    }

    void showCriticalPatients() {
        int idx = 0;
        System.out.println("Critical Patients:");
        while(idx < totalPatients) {
            if(patientList[idx].evaluateHealth().equals("Critical"))
                System.out.println(patientList[idx].getPatientId() + ", " 
                                   + patientList[idx].getName() + ", " 
                                   + patientList[idx].getPatientType());
            idx++;
        }
    }

    void evaluateSinglePatient(int index) {
        Patient p = patientList[index];
        System.out.println("Patient: " + p.getName() + ", Type: " + p.getPatientType() 
                           + ", Status: " + p.evaluateHealth() 
                           + ", Monitor Every: " + p.getMonitoringFrequency() + " mins");
    }

    void showReport() {
        int idx = 0;
        while(idx < totalPatients) {
            System.out.println(patientList[idx].getPatientId() + ", " 
                               + patientList[idx].getName() + ", " 
                               + patientList[idx].getPatientType() + ", " 
                               + patientList[idx].evaluateHealth() + ", Monitor: " 
                               + patientList[idx].getMonitoringFrequency() + " mins");
            idx++;
        }
        System.out.println("Total Critical: " + countCritical());
        showCriticalPatients();
    }
}

public class Task2Lab8 {
    public static void main(String args[]) {
        Patient patientList[] = new Patient[5];
        patientList[0] = new CardiacPatient("P001", "Kamran Shah", 55, 130, 98.6, 3, 185, 110);
        patientList[1] = new InfectiousPatient("P002", "Nadia Farooq", 30, 85, 104.2, 2, "Typhoid", true);
        patientList[2] = new CardiacPatient("P003", "Rehan Malik", 60, 95, 97.8, 1, 130, 85);
        patientList[3] = new InfectiousPatient("P004", "Sana Akram", 25, 78, 99.5, 1, "Flu", false);
        patientList[4] = new CardiacPatient("P005", "Faisal Iqbal", 48, 110, 98.2, 2, 150, 95);

        HospitalMonitor monitor = new HospitalMonitor(patientList, 5);
        monitor.showReport();

        System.out.println();
        monitor.evaluateSinglePatient(3);
    }
}
