import java.util.ArrayList;

abstract class Automobile {
    private String plateNo;

    Automobile(String plateNo) {
        this.plateNo = plateNo;
    }

    void setPlateNo(String plateNo) {
        this.plateNo = plateNo;
    }
    String getPlateNo() {
        return plateNo;
    }

    abstract String kind();
    abstract String requiredSlotType();
    abstract int hourlyRate();
    abstract int additionalFee();
}

class Motorcycle extends Automobile {
    Motorcycle(String plateNo) {
        super(plateNo);
    }

    String kind() {
        return "Bike";
    }
    String requiredSlotType() {
        return "Small";
    }
    int hourlyRate() {
        return 20;
    }
    int additionalFee() {
        return 0;
    }
}

class Sedan extends Automobile {
    Sedan(String plateNo) {
        super(plateNo);
    }

    String kind() {
        return "Car";
    }
    String requiredSlotType() {
        return "Medium";
    }
    int hourlyRate() {
        return 50;
    }
    int additionalFee() {
        return 0;
    }
}

class HeavyVehicle extends Automobile {
    HeavyVehicle(String plateNo) {
        super(plateNo);
    }

    String kind() {
        return "Truck";
    }
    String requiredSlotType() {
        return "Large";
    }
    int hourlyRate() {
        return 100;
    }
    int additionalFee() {
        return 200;
    }
}

class Spot {
    private String spotCode;
    private String category;
    private boolean taken;
    private Automobile currentVehicle;

    Spot(String spotCode, String category) {
        this.spotCode = spotCode;
        this.category = category;
        this.taken = false;
        this.currentVehicle = null;
    }

    void setSpotCode(String spotCode) {
        this.spotCode = spotCode;
    }
    String getSpotCode() {
        return spotCode;
    }

    void setCategory(String category) {
        this.category = category;
    }
    String getCategory() {
        return category;
    }

    boolean isTaken() {
        return taken;
    }

    Automobile getCurrentVehicle() {
        return currentVehicle;
    }

    void occupy(Automobile a) {
        this.currentVehicle = a;
        this.taken = true;
    }

    void vacate() {
        this.currentVehicle = null;
        this.taken = false;
    }
}

class Ticket {
    private Automobile auto;
    private Spot assignedSpot;
    private String timeIn;
    private String timeOut;
    private int hrs;
    private int charge;

    Ticket(Automobile auto, Spot assignedSpot, String timeIn) {
        this.auto = auto;
        this.assignedSpot = assignedSpot;
        this.timeIn = timeIn;
        this.timeOut = null;
        this.hrs = 0;
        this.charge = 0;
    }

    void setAuto(Automobile auto) {
        this.auto = auto;
    }
    Automobile getAuto() {
        return auto;
    }

    void setAssignedSpot(Spot assignedSpot) {
        this.assignedSpot = assignedSpot;
    }
    Spot getAssignedSpot() {
        return assignedSpot;
    }

    void setTimeIn(String timeIn) {
        this.timeIn = timeIn;
    }
    String getTimeIn() {
        return timeIn;
    }

    void setTimeOut(String timeOut) {
        this.timeOut = timeOut;
    }
    String getTimeOut() {
        return timeOut;
    }

    void setHrs(int hrs) {
        this.hrs = hrs;
    }
    int getHrs() {
        return hrs;
    }

    void setCharge(int charge) {
        this.charge = charge;
    }
    int getCharge() {
        return charge;
    }
}

class Garage {
    private ArrayList<Spot> allSpots;
    private ArrayList<Ticket> allTickets;

    Garage() {
        this.allSpots = new ArrayList<>();
        this.allTickets = new ArrayList<>();
    }

    void addSpot(Spot s) {
        allSpots.add(s);
    }

    ArrayList<Spot> getAllSpots() {
        return allSpots;
    }

    ArrayList<Ticket> getAllTickets() {
        return allTickets;
    }

    Spot locateFreeSpot(String type) {
        int k = 0;
        while (k < allSpots.size()) {
            Spot sp = allSpots.get(k);
            if (sp.isTaken() == false && sp.getCategory().equals(type)) {
                return sp;
            }
            k++;
        }
        return null;
    }

    Ticket enterParking(Automobile a, String timeIn) {
        Spot freeSpot = locateFreeSpot(a.requiredSlotType());
        if (freeSpot == null) {
            System.out.println("Sorry, no " + a.requiredSlotType() + " spot available for " + a.getPlateNo());
            return null;
        }
        freeSpot.occupy(a);
        Ticket t = new Ticket(a, freeSpot, timeIn);
        allTickets.add(t);
        return t;
    }

    Ticket leaveParking(Automobile a, String timeOut, int hrs) {
        int k = 0;
        while (k < allTickets.size()) {
            Ticket t = allTickets.get(k);
            if (t.getAuto().getPlateNo().equals(a.getPlateNo()) && t.getTimeOut() == null) {
                t.setTimeOut(timeOut);
                t.setHrs(hrs);

                int base = hrs * a.hourlyRate();
                int fee = a.additionalFee();
                t.setCharge(base + fee);

                t.getAssignedSpot().vacate();
                return t;
            }
            k++;
        }
        return null;
    }

    int countFreeSpots() {
        int n = 0;
        int k = 0;
        while (k < allSpots.size()) {
            if (allSpots.get(k).isTaken() == false) {
                n++;
            }
            k++;
        }
        return n;
    }

    int countTotalParked() {
        return allTickets.size();
    }
}

public class Task2Lab10 {
    public static void main(String args[]) {
        Garage garage = new Garage();

        garage.addSpot(new Spot("S1", "Small"));
        garage.addSpot(new Spot("S2", "Small"));
        garage.addSpot(new Spot("S3", "Small"));
        garage.addSpot(new Spot("M1", "Medium"));
        garage.addSpot(new Spot("M2", "Medium"));
        garage.addSpot(new Spot("M3", "Medium"));
        garage.addSpot(new Spot("M4", "Medium"));
        garage.addSpot(new Spot("L1", "Large"));
        garage.addSpot(new Spot("L2", "Large"));
        garage.addSpot(new Spot("L3", "Large"));

        Motorcycle m = new Motorcycle("BK-101");
        Sedan s = new Sedan("CAR-202");
        HeavyVehicle h = new HeavyVehicle("TRK-303");

        System.out.println("========== SMART PARKING SYSTEM ==========");
        System.out.println();

        Ticket t1 = garage.enterParking(m, "10:00 AM");
        System.out.println("Vehicle Entered:");
        System.out.println("Type: " + m.kind());
        System.out.println("Number: " + m.getPlateNo());
        System.out.println();
        System.out.println("Assigned Slot: " + t1.getAssignedSpot().getSpotCode()
                         + " (" + t1.getAssignedSpot().getCategory() + " Slot)");
        System.out.println("Entry Time: " + t1.getTimeIn());
        System.out.println();
        System.out.println("-----------------------------------------");
        System.out.println();

        Ticket t2 = garage.enterParking(s, "10:05 AM");
        System.out.println("Vehicle Entered:");
        System.out.println("Type: " + s.kind());
        System.out.println("Number: " + s.getPlateNo());
        System.out.println();
        System.out.println("Assigned Slot: " + t2.getAssignedSpot().getSpotCode()
                         + " (" + t2.getAssignedSpot().getCategory() + " Slot)");
        System.out.println("Entry Time: " + t2.getTimeIn());
        System.out.println();
        System.out.println("-----------------------------------------");
        System.out.println();

        Ticket t3 = garage.enterParking(h, "10:10 AM");
        System.out.println("Vehicle Entered:");
        System.out.println("Type: " + h.kind());
        System.out.println("Number: " + h.getPlateNo());
        System.out.println();
        System.out.println("Assigned Slot: " + t3.getAssignedSpot().getSpotCode()
                         + " (" + t3.getAssignedSpot().getCategory() + " Slot)");
        System.out.println("Entry Time: " + t3.getTimeIn());
        System.out.println();
        System.out.println("=========================================");
        System.out.println("            VEHICLE EXIT");
        System.out.println("=========================================");
        System.out.println();

        Ticket e1 = garage.leaveParking(m, "12:00 PM", 2);
        System.out.println("Vehicle: " + e1.getAuto().getPlateNo() + " (" + e1.getAuto().kind() + ")");
        System.out.println("Exit Time: " + e1.getTimeOut());
        System.out.println("Duration: " + e1.getHrs() + " hours");
        System.out.println();
        System.out.println("--- Bill Breakdown ---");
        System.out.println("Rate: " + e1.getAuto().hourlyRate() + "/hour");
        System.out.println("Total = " + e1.getHrs() + " x " + e1.getAuto().hourlyRate()
                         + " = " + e1.getCharge() + " PKR");
        System.out.println();
        System.out.println("-----------------------------------------");
        System.out.println();

        Ticket e2 = garage.leaveParking(s, "1:05 PM", 3);
        System.out.println("Vehicle: " + e2.getAuto().getPlateNo() + " (" + e2.getAuto().kind() + ")");
        System.out.println("Exit Time: " + e2.getTimeOut());
        System.out.println("Duration: " + e2.getHrs() + " hours");
        System.out.println();
        System.out.println("--- Bill Breakdown ---");
        System.out.println("Rate: " + e2.getAuto().hourlyRate() + "/hour");
        System.out.println("Total = " + e2.getHrs() + " x " + e2.getAuto().hourlyRate()
                         + " = " + e2.getCharge() + " PKR");
        System.out.println();
        System.out.println("-----------------------------------------");
        System.out.println();

        Ticket e3 = garage.leaveParking(h, "2:10 PM", 4);
        System.out.println("Vehicle: " + e3.getAuto().getPlateNo() + " (" + e3.getAuto().kind() + ")");
        System.out.println("Exit Time: " + e3.getTimeOut());
        System.out.println("Duration: " + e3.getHrs() + " hours");
        System.out.println();
        System.out.println("--- Bill Breakdown ---");
        System.out.println("Rate: " + e3.getAuto().hourlyRate() + "/hour");
        System.out.println("Extra Space Charge = " + e3.getAuto().additionalFee());
        System.out.println("Total = (" + e3.getHrs() + " x " + e3.getAuto().hourlyRate()
                         + ") + " + e3.getAuto().additionalFee() + " = " + e3.getCharge() + " PKR");
        System.out.println();
        System.out.println("=========================================");
        System.out.println("Summary:");
        System.out.println("Total Vehicles Parked: " + garage.countTotalParked());
        System.out.println("Available Slots Remaining: " + garage.countFreeSpots());
    }
}
