import java.util.ArrayList;

abstract class Vehicle {
    private String number;

    Vehicle(String number) {
        this.number = number;
    }

    void setNumber(String number) { 
        this.number = number; 
    }
    String getNumber() { 
        return number; 
    }

    abstract String getType();
    abstract String getSlotSize();
    abstract int getRatePerHour();
    abstract int getExtraCharges();
}

class Bike extends Vehicle {
    Bike(String number) {
        super(number);
    }

    String getType() { 
        return "Bike"; 
    }

    String getSlotSize() { 
        return "Small"; 
    }

    int getRatePerHour() { 
        return 20; 
    }

    int getExtraCharges() { 
        return 0; 
    }
}

class Car extends Vehicle {
    Car(String number) {
        super(number);
    }

    String getType() { 
        return "Car"; 
    }

    String getSlotSize() { 
        return "Medium"; 
    }

    int getRatePerHour() { 
        return 50; 
    }

    int getExtraCharges() { 
        return 0; 
    }
}

class Truck extends Vehicle {
    Truck(String number) {
        super(number);
    }

    String getType() { 
        return "Truck"; 
    }

    String getSlotSize() { 
        return "Large"; 
    }

    int getRatePerHour() { 
        return 100; 
    }

    int getExtraCharges() { 
        return 200; 
    }
}

class ParkingSlot {
    private String slotId;
    private String size;
    private boolean occupied;
    private Vehicle parkedVehicle;

    ParkingSlot(String slotId, String size) {
        this.slotId = slotId;
        this.size = size;
        this.occupied = false;
        this.parkedVehicle = null;
    }

    void setSlotId(String slotId) { 
        this.slotId = slotId; 
    }
    String getSlotId() { 
        return slotId; 
    }

    void setSize(String size) { 
        this.size = size; 
    }
    String getSize() { 
        return size; 
    }

    boolean isOccupied() { 
        return occupied; 
    }

    Vehicle getParkedVehicle() { 
        return parkedVehicle; 
    }

    void parkVehicle(Vehicle v) {
        this.parkedVehicle = v;
        this.occupied = true;
    }

    void removeVehicle() {
        this.parkedVehicle = null;
        this.occupied = false;
    }
}

class ParkingRecord {
    private Vehicle vehicle;
    private ParkingSlot slot;
    private String entryTime;
    private String exitTime;
    private int duration;
    private int totalBill;

    ParkingRecord(Vehicle vehicle, ParkingSlot slot, String entryTime) {
        this.vehicle = vehicle;
        this.slot = slot;
        this.entryTime = entryTime;
        this.exitTime = null;
        this.duration = 0;
        this.totalBill = 0;
    }

    void setVehicle(Vehicle vehicle) { 
        this.vehicle = vehicle; 
    }
    Vehicle getVehicle() { 
        return vehicle; 
    }

    void setSlot(ParkingSlot slot) { 
        this.slot = slot; 
    }
    ParkingSlot getSlot() { 
        return slot; 
    }

    void setEntryTime(String entryTime) { 
        this.entryTime = entryTime; 
    }
    String getEntryTime() { 
        return entryTime; 
    }

    void setExitTime(String exitTime) { 
        this.exitTime = exitTime; 
    }
    String getExitTime() { 
        return exitTime; 
    }

    void setDuration(int duration) { 
        this.duration = duration; 
    }
    int getDuration() { 
        return duration; 
    }

    void setTotalBill(int totalBill) { 
        this.totalBill = totalBill; 
    }
    int getTotalBill() { 
        return totalBill; 
    }
}

class ParkingLot {
    private ArrayList<ParkingSlot> slots;
    private ArrayList<ParkingRecord> history;

    ParkingLot() {
        this.slots = new ArrayList<>();
        this.history = new ArrayList<>();
    }

    ArrayList<ParkingSlot> getSlots() { 
        return slots; 
    }

    ArrayList<ParkingRecord> getHistory() { 
        return history; 
    }

    void addSlot(ParkingSlot slot) {
        slots.add(slot);
    }

    ParkingSlot findAvailableSlot(String size) {
        int i = 0;
        while (i < slots.size()) {
            ParkingSlot s = slots.get(i);
            if (!s.isOccupied() && s.getSize().equals(size)) {
                return s;
            }
            i++;
        }
        return null;
    }

    ParkingRecord parkVehicle(Vehicle v, String entryTime) {
        ParkingSlot slot = findAvailableSlot(v.getSlotSize());
        if (slot == null) {
            System.out.println("No available " + v.getSlotSize() + " slot for " + v.getNumber());
            return null;
        }
        slot.parkVehicle(v);
        ParkingRecord record = new ParkingRecord(v, slot, entryTime);
        history.add(record);
        return record;
    }

    ParkingRecord exitVehicle(Vehicle v, String exitTime, int duration) {
        int i = 0;
        while (i < history.size()) {
            ParkingRecord rec = history.get(i);
            if (rec.getVehicle().getNumber().equals(v.getNumber()) && rec.getExitTime() == null) {
                rec.setExitTime(exitTime);
                rec.setDuration(duration);

                int baseCost = duration * v.getRatePerHour();
                int extra = v.getExtraCharges();
                int total = baseCost + extra;
                rec.setTotalBill(total);

                rec.getSlot().removeVehicle();
                return rec;
            }
            i++;
        }
        return null;
    }

    int getAvailableSlotCount() {
        int count = 0;
        int i = 0;
        while (i < slots.size()) {
            if (!slots.get(i).isOccupied()) {
                count++;
            }
            i++;
        }
        return count;
    }

    int getTotalVehiclesParked() {
        return history.size();
    }
}

public class Task2Lab10 {
    public static void main(String args[]) {
        ParkingLot lot = new ParkingLot();

        lot.addSlot(new ParkingSlot("S1", "Small"));
        lot.addSlot(new ParkingSlot("S2", "Small"));
        lot.addSlot(new ParkingSlot("S3", "Small"));
        lot.addSlot(new ParkingSlot("M1", "Medium"));
        lot.addSlot(new ParkingSlot("M2", "Medium"));
        lot.addSlot(new ParkingSlot("M3", "Medium"));
        lot.addSlot(new ParkingSlot("M4", "Medium"));
        lot.addSlot(new ParkingSlot("L1", "Large"));
        lot.addSlot(new ParkingSlot("L2", "Large"));
        lot.addSlot(new ParkingSlot("L3", "Large"));

        Bike bike = new Bike("BK-101");
        Car car = new Car("CAR-202");
        Truck truck = new Truck("TRK-303");

        System.out.println("========== SMART PARKING SYSTEM ==========");
        System.out.println();

        ParkingRecord r1 = lot.parkVehicle(bike, "10:00 AM");
        System.out.println("Vehicle Entered:");
        System.out.println("Type: " + bike.getType());
        System.out.println("Number: " + bike.getNumber());
        System.out.println();
        System.out.println("Assigned Slot: " + r1.getSlot().getSlotId() + " (" + r1.getSlot().getSize() + " Slot)");
        System.out.println("Entry Time: " + r1.getEntryTime());
        System.out.println();
        System.out.println("-----------------------------------------");
        System.out.println();

        ParkingRecord r2 = lot.parkVehicle(car, "10:05 AM");
        System.out.println("Vehicle Entered:");
        System.out.println("Type: " + car.getType());
        System.out.println("Number: " + car.getNumber());
        System.out.println();
        System.out.println("Assigned Slot: " + r2.getSlot().getSlotId() + " (" + r2.getSlot().getSize() + " Slot)");
        System.out.println("Entry Time: " + r2.getEntryTime());
        System.out.println();
        System.out.println("-----------------------------------------");
        System.out.println();

        ParkingRecord r3 = lot.parkVehicle(truck, "10:10 AM");
        System.out.println("Vehicle Entered:");
        System.out.println("Type: " + truck.getType());
        System.out.println("Number: " + truck.getNumber());
        System.out.println();
        System.out.println("Assigned Slot: " + r3.getSlot().getSlotId() + " (" + r3.getSlot().getSize() + " Slot)");
        System.out.println("Entry Time: " + r3.getEntryTime());
        System.out.println();
        System.out.println("=========================================");
        System.out.println("            VEHICLE EXIT");
        System.out.println("=========================================");
        System.out.println();

        ParkingRecord exit1 = lot.exitVehicle(bike, "12:00 PM", 2);
        System.out.println("Vehicle: " + exit1.getVehicle().getNumber() + " (" + exit1.getVehicle().getType() + ")");
        System.out.println("Exit Time: " + exit1.getExitTime());
        System.out.println("Duration: " + exit1.getDuration() + " hours");
        System.out.println();
        System.out.println("--- Bill Breakdown ---");
        System.out.println("Rate: " + exit1.getVehicle().getRatePerHour() + "/hour");
        System.out.println("Total = " + exit1.getDuration() + " x " + exit1.getVehicle().getRatePerHour()
                         + " = " + exit1.getTotalBill() + " PKR");
        System.out.println();
        System.out.println("-----------------------------------------");
        System.out.println();

        ParkingRecord exit2 = lot.exitVehicle(car, "1:05 PM", 3);
        System.out.println("Vehicle: " + exit2.getVehicle().getNumber() + " (" + exit2.getVehicle().getType() + ")");
        System.out.println("Exit Time: " + exit2.getExitTime());
        System.out.println("Duration: " + exit2.getDuration() + " hours");
        System.out.println();
        System.out.println("--- Bill Breakdown ---");
        System.out.println("Rate: " + exit2.getVehicle().getRatePerHour() + "/hour");
        System.out.println("Total = " + exit2.getDuration() + " x " + exit2.getVehicle().getRatePerHour()
                         + " = " + exit2.getTotalBill() + " PKR");
        System.out.println();
        System.out.println("-----------------------------------------");
        System.out.println();

        ParkingRecord exit3 = lot.exitVehicle(truck, "2:10 PM", 4);
        System.out.println("Vehicle: " + exit3.getVehicle().getNumber() + " (" + exit3.getVehicle().getType() + ")");
        System.out.println("Exit Time: " + exit3.getExitTime());
        System.out.println("Duration: " + exit3.getDuration() + " hours");
        System.out.println();
        System.out.println("--- Bill Breakdown ---");
        System.out.println("Rate: " + exit3.getVehicle().getRatePerHour() + "/hour");
        System.out.println("Extra Space Charge = " + exit3.getVehicle().getExtraCharges());
        int baseCost = exit3.getDuration() * exit3.getVehicle().getRatePerHour();
        System.out.println("Total = (" + exit3.getDuration() + " x " + exit3.getVehicle().getRatePerHour()
                         + ") + " + exit3.getVehicle().getExtraCharges() + " = " + exit3.getTotalBill() + " PKR");
        System.out.println();
        System.out.println("=========================================");
        System.out.println("Summary:");
        System.out.println("Total Vehicles Parked: " + lot.getTotalVehiclesParked());
        System.out.println("Available Slots Remaining: " + lot.getAvailableSlotCount());
    }
}
