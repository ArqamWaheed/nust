class Vehicle {
    String plateNumber;
    String driverName;
    double recordedSpeed;
    double speedLimit;
    int pastViolations;

    Vehicle(String plateNumber, String driverName, double recordedSpeed, double speedLimit, int pastViolations) {
        this.plateNumber = plateNumber;
        this.driverName = driverName;
        this.recordedSpeed = recordedSpeed;
        this.speedLimit = speedLimit;
        this.pastViolations = pastViolations;
    }

    void setPlateNumber(String plateNumber) { 
        this.plateNumber = plateNumber; 
    }
    String getPlateNumber() { 
        return plateNumber; 
    }

    void setDriverName(String driverName) { 
        this.driverName = driverName; 
    }
    String getDriverName() { 
        return driverName; 
    }

    void setRecordedSpeed(double recordedSpeed) { 
        this.recordedSpeed = recordedSpeed; 
    }
    double getRecordedSpeed() { 
        return recordedSpeed; 
    }

    void setSpeedLimit(double speedLimit) { 
        this.speedLimit = speedLimit; 
    }
    double getSpeedLimit() { 
        return speedLimit; 
    }

    void setPastViolations(int pastViolations) { 
        this.pastViolations = pastViolations; 
    }
    int getPastViolations() { 
        return pastViolations; 
    }

    boolean hasViolation() {
        return recordedSpeed > speedLimit;
    }

    double calcFineAmount() {
        if(!hasViolation())
            return 0;
        double amount = 0;
        double overSpeed = recordedSpeed - speedLimit;
        if(overSpeed <= 20)
            amount = 1000;
        else
            amount = 2500;
        amount = amount + (pastViolations * 500);
        return amount;
    }
}

class TrafficMonitor {
    Vehicle vehicleRecords[];
    int numVehicles;

    TrafficMonitor(Vehicle vehicleRecords[], int numVehicles) {
        this.vehicleRecords = vehicleRecords;
        this.numVehicles = numVehicles;
    }

    Vehicle findMaxFineVehicle() {
        Vehicle maxFine = vehicleRecords[0];
        int idx = 1;
        while(idx < numVehicles) {
            if(vehicleRecords[idx].calcFineAmount() > maxFine.calcFineAmount())
                maxFine = vehicleRecords[idx];
            idx++;
        }
        return maxFine;
    }

    double calcTotalFineCollected() {
        double sum = 0;
        int idx = 0;
        while(idx < numVehicles) {
            sum = sum + vehicleRecords[idx].calcFineAmount();
            idx++;
        }
        return sum;
    }

    void showViolationSummary() {
        int idx = 0;
        while(idx < numVehicles) {
            System.out.println(vehicleRecords[idx].getPlateNumber() + ", " + vehicleRecords[idx].getDriverName() 
                               + ", " + vehicleRecords[idx].getRecordedSpeed() + "/" + vehicleRecords[idx].getSpeedLimit() 
                               + ", " + (vehicleRecords[idx].hasViolation() ? "Violation" : "No Violation") 
                               + ", Fine: " + vehicleRecords[idx].calcFineAmount() 
                               + ", Previous: " + vehicleRecords[idx].getPastViolations());
            idx++;
        }
        System.out.println("Total Fines: " + calcTotalFineCollected());
        Vehicle maxFine = findMaxFineVehicle();
        System.out.println("Highest Fine: " + maxFine.getPlateNumber() + ", " + maxFine.getDriverName() + ", " + maxFine.calcFineAmount());
    }
}

public class Task2 {
    public static void main(String args[]) {
        Vehicle vehicleRecords[] = new Vehicle[5];
        vehicleRecords[0] = new Vehicle("LHR-4521", "Hamza Malik", 85, 60, 1);
        vehicleRecords[1] = new Vehicle("ISB-7832", "Zainab Aslam", 58, 60, 0);
        vehicleRecords[2] = new Vehicle("KHI-1190", "Faizan Ahmed", 95, 70, 3);
        vehicleRecords[3] = new Vehicle("RWP-3345", "Mehwish Hayat", 110, 80, 2);
        vehicleRecords[4] = new Vehicle("PSH-6678", "Asad Umar", 72, 60, 0);

        TrafficMonitor monitor = new TrafficMonitor(vehicleRecords, 5);
        monitor.showViolationSummary();

        System.out.println(vehicleRecords[1].getPlateNumber() + ", " + vehicleRecords[1].hasViolation() + ", Fine: " + vehicleRecords[1].calcFineAmount());
    }
}
