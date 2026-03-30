class Patient {
    String id;
    String patientName;
    double bodyTemp;
    int pulse;

    Patient(String id, String patientName, double bodyTemp, int pulse) {
        this.id = id;
        this.patientName = patientName;
        this.bodyTemp = bodyTemp;
        this.pulse = pulse;
    }

    void setId(String id) { 
        this.id = id; 
    }
    String getId() { 
        return id; 
    }

    void setPatientName(String patientName) { 
        this.patientName = patientName; 
    }
    String getPatientName() { 
        return patientName; 
    }

    void setBodyTemp(double bodyTemp) { 
        this.bodyTemp = bodyTemp; 
    }
    double getBodyTemp() { 
        return bodyTemp; 
    }

    void setPulse(int pulse) { 
        this.pulse = pulse; 
    }
    int getPulse() { 
        return pulse; 
    }

    boolean checkFever() {
        return bodyTemp > 99;
    }

    boolean checkCritical() {
        return pulse < 50 || pulse > 120;
    }

    String getCondition() {
        if(checkCritical() && checkFever())
            return "Critical + Fever";
        else if(checkCritical())
            return "Critical";
        else if(checkFever())
            return "Fever";
        else
            return "Normal";
    }
}

class PatientMonitor {
    Patient patientRecords[];
    int numPatients;

    PatientMonitor(Patient patientRecords[], int numPatients) {
        this.patientRecords = patientRecords;
        this.numPatients = numPatients;
    }

    int countCritical() {
        int cnt = 0;
        int idx = 0;
        while(idx < numPatients) {
            if(patientRecords[idx].checkCritical())
                cnt++;
            idx++;
        }
        return cnt;
    }

    void showFeverPatients() {
        int idx = 0;
        while(idx < numPatients) {
            if(patientRecords[idx].checkFever())
                System.out.println("Fever: " + patientRecords[idx].getPatientName() + ", " + patientRecords[idx].getBodyTemp());
            idx++;
        }
    }

    void displayReport() {
        int idx = 0;
        while(idx < numPatients) {
            System.out.println(patientRecords[idx].getId() + ", " + patientRecords[idx].getPatientName() 
                               + ", " + patientRecords[idx].getBodyTemp() + ", " + patientRecords[idx].getPulse() 
                               + ", " + patientRecords[idx].getCondition());
            idx++;
        }
        System.out.println("Critical Patients: " + countCritical());
        showFeverPatients();
    }
}

public class Task4 {
    public static void main(String args[]) {
        Patient patientRecords[] = new Patient[5];
        patientRecords[0] = new Patient("PT01", "Farhan Saeed", 100.8, 78);
        patientRecords[1] = new Patient("PT02", "Saba Qamar", 97.9, 48);
        patientRecords[2] = new Patient("PT03", "Wahab Riaz", 101.3, 125);
        patientRecords[3] = new Patient("PT04", "Amna Ilyas", 98.2, 90);
        patientRecords[4] = new Patient("PT05", "Shahid Afridi", 99.5, 68);

        PatientMonitor monitor = new PatientMonitor(patientRecords, 5);
        monitor.displayReport();

        System.out.println(patientRecords[0].getPatientName() + ", Fever: " + patientRecords[0].checkFever() + ", Critical: " + patientRecords[0].checkCritical());
    }
}
