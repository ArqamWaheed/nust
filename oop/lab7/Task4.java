class Patient {
    String patientId;
    String name;
    double temperature;
    int heartRate;

    Patient(String patientId, String name, double temperature, int heartRate) {
        this.patientId = patientId;
        this.name = name;
        this.temperature = temperature;
        this.heartRate = heartRate;
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

    void setTemperature(double temperature) { 
        this.temperature = temperature; 
    }
    double getTemperature() { 
        return temperature; 
    }

    void setHeartRate(int heartRate) { 
        this.heartRate = heartRate; 
    }
    int getHeartRate() { 
        return heartRate; 
    }

    boolean hasFever() {
        return temperature > 99;
    }

    boolean isCritical() {
        return heartRate < 50 || heartRate > 120;
    }

    String getHealthStatus() {
        if(isCritical() && hasFever())
            return "Critical + Fever";
        else if(isCritical())
            return "Critical";
        else if(hasFever())
            return "Fever";
        else
            return "Normal";
    }
}

class PatientMonitor {
    Patient patients[];
    int patientCount;

    PatientMonitor(Patient patients[], int patientCount) {
        this.patients = patients;
        this.patientCount = patientCount;
    }

    int countCriticalPatients() {
        int count = 0;
        int i = 0;
        while(i < patientCount) {
            if(patients[i].isCritical())
                count++;
            i++;
        }
        return count;
    }

    void displayFeverPatients() {
        System.out.println("Patients with Fever:");
        int i = 0;
        int found = 0;
        while(i < patientCount) {
            if(patients[i].hasFever()) {
                System.out.println("  - " + patients[i].getName() + " (Temp: " + patients[i].getTemperature() + ")");
                found++;
            }
            i++;
        }
        if(found == 0)
            System.out.println("  None");
    }

    void printMonitoringReport() {
        System.out.println("========================================");
        System.out.println("   PATIENT MONITORING REPORT");
        System.out.println("========================================");
        int i = 0;
        while(i < patientCount) {
            System.out.println("Patient ID: " + patients[i].getPatientId());
            System.out.println("Name: " + patients[i].getName());
            System.out.println("Temperature: " + patients[i].getTemperature());
            System.out.println("Heart Rate: " + patients[i].getHeartRate());
            System.out.println("Status: " + patients[i].getHealthStatus());
            System.out.println("----------------------------------------");
            i++;
        }
        System.out.println("Critical Patients: " + countCriticalPatients());
        System.out.println();
        displayFeverPatients();
        System.out.println("========================================");
    }
}

public class Task4 {
    public static void main(String args[]) {
        Patient patients[] = new Patient[4];
        patients[0] = new Patient("P001", "Ahmed Khan", 101.5, 85);
        patients[1] = new Patient("P002", "Sara Ali", 98.6, 45);
        patients[2] = new Patient("P003", "Bilal Shah", 100.2, 130);
        patients[3] = new Patient("P004", "Nadia Raza", 97.8, 72);

        PatientMonitor monitor = new PatientMonitor(patients, 4);
        monitor.printMonitoringReport();

        System.out.println();
        System.out.println("Checking individual patient:");
        System.out.println("Patient: " + patients[0].getName());
        System.out.println("Has Fever: " + patients[0].hasFever());
        System.out.println("Is Critical: " + patients[0].isCritical());
    }
}
