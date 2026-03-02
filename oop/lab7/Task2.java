class Vehicle {
    String vehicleNumber;
    String ownerName;
    double speedRecorded;
    double allowedSpeed;
    int previousViolations;

    Vehicle(String vehicleNumber, String ownerName, double speedRecorded, double allowedSpeed, int previousViolations) {
        this.vehicleNumber = vehicleNumber;
        this.ownerName = ownerName;
        this.speedRecorded = speedRecorded;
        this.allowedSpeed = allowedSpeed;
        this.previousViolations = previousViolations;
    }

    void setVehicleNumber(String vehicleNumber) { 
        this.vehicleNumber = vehicleNumber; 
    }
    String getVehicleNumber() { 
        return vehicleNumber; 
    }

    void setOwnerName(String ownerName) { 
        this.ownerName = ownerName; 
    }
    String getOwnerName() { 
        return ownerName; 
    }

    void setSpeedRecorded(double speedRecorded) { 
        this.speedRecorded = speedRecorded; 
    }
    double getSpeedRecorded() { 
        return speedRecorded; 
    }

    void setAllowedSpeed(double allowedSpeed) { 
        this.allowedSpeed = allowedSpeed; 
    }
    double getAllowedSpeed() { 
        return allowedSpeed; 
    }

    void setPreviousViolations(int previousViolations) { 
        this.previousViolations = previousViolations; 
    }
    int getPreviousViolations() { 
        return previousViolations; 
    }

    boolean isViolation() {
        return speedRecorded > allowedSpeed;
    }

    double calcFine() {
        if(!isViolation())
            return 0;
        double fine = 0;
        double excessSpeed = speedRecorded - allowedSpeed;
        if(excessSpeed <= 20)
            fine = 1000;
        else
            fine = 2500;
        fine = fine + (previousViolations * 500);
        return fine;
    }
}

class TrafficMonitor {
    Vehicle vehicles[];
    int vehicleCount;

    TrafficMonitor(Vehicle vehicles[], int vehicleCount) {
        this.vehicles = vehicles;
        this.vehicleCount = vehicleCount;
    }

    Vehicle findHighestFineVehicle() {
        Vehicle highest = vehicles[0];
        int i = 1;
        while(i < vehicleCount) {
            if(vehicles[i].calcFine() > highest.calcFine())
                highest = vehicles[i];
            i++;
        }
        return highest;
    }

    double calcTotalFines() {
        double total = 0;
        int i = 0;
        while(i < vehicleCount) {
            total = total + vehicles[i].calcFine();
            i++;
        }
        return total;
    }

    void printViolationReport() {
        System.out.println("========================================");
        System.out.println("   TRAFFIC VIOLATION SUMMARY REPORT");
        System.out.println("========================================");
        int i = 0;
        while(i < vehicleCount) {
            System.out.println("Vehicle: " + vehicles[i].getVehicleNumber());
            System.out.println("Owner: " + vehicles[i].getOwnerName());
            System.out.println("Speed: " + vehicles[i].getSpeedRecorded() + " km/h (Limit: " + vehicles[i].getAllowedSpeed() + " km/h)");
            if(vehicles[i].isViolation()) {
                System.out.println("Status: VIOLATION");
                System.out.println("Fine: Rs. " + vehicles[i].calcFine());
            }
            else {
                System.out.println("Status: No Violation");
                System.out.println("Fine: Rs. 0");
            }
            System.out.println("Previous Violations: " + vehicles[i].getPreviousViolations());
            System.out.println("----------------------------------------");
            i++;
        }
        System.out.println("Total Fines Collected: Rs. " + calcTotalFines());
        Vehicle highest = findHighestFineVehicle();
        System.out.println("Highest Fine: " + highest.getVehicleNumber() 
                           + " (" + highest.getOwnerName() + ") - Rs. " + highest.calcFine());
        System.out.println("========================================");
    }
}

public class Task2 {
    public static void main(String args[]) {
        Vehicle vehicles[] = new Vehicle[4];
        vehicles[0] = new Vehicle("ABC-123", "Ali Raza", 90, 60, 2);
        vehicles[1] = new Vehicle("DEF-456", "Sara Khan", 55, 60, 0);
        vehicles[2] = new Vehicle("GHI-789", "Usman Shah", 75, 60, 1);
        vehicles[3] = new Vehicle("JKL-012", "Nadia Butt", 100, 60, 3);

        TrafficMonitor monitor = new TrafficMonitor(vehicles, 4);
        monitor.printViolationReport();

        System.out.println();
        System.out.println("Checking individual vehicle:");
        System.out.println("Vehicle: " + vehicles[1].getVehicleNumber());
        System.out.println("Violation: " + vehicles[1].isViolation());
        System.out.println("Fine: Rs. " + vehicles[1].calcFine());
    }
}
