import java.util.ArrayList;

class HospitalPatient {
    private String name;
    private String birthDate;
    private String gender;
    private String dateAccepted;
    private String report;
    private Doctor treatingDoctor;
    private int daysToStay;

    HospitalPatient(String name, String birthDate, String gender, String dateAccepted,
                    String report, Doctor treatingDoctor, int daysToStay) {
        this.name = name;
        this.birthDate = birthDate;
        this.gender = gender;
        this.dateAccepted = dateAccepted;
        this.report = report;
        this.treatingDoctor = treatingDoctor;
        this.daysToStay = daysToStay;
    }

    void setName(String name) { 
        this.name = name; 
    }
    String getName() { 
        return name; 
    }

    void setBirthDate(String birthDate) { 
        this.birthDate = birthDate; 
    }
    String getBirthDate() { 
        return birthDate; 
    }

    void setGender(String gender) { 
        this.gender = gender; 
    }
    String getGender() { 
        return gender; 
    }

    void setDateAccepted(String dateAccepted) { 
        this.dateAccepted = dateAccepted; 
    }
    String getDateAccepted() { 
        return dateAccepted; 
    }

    void setReport(String report) { 
        this.report = report; 
    }
    String getReport() { 
        return report; 
    }

    void setTreatingDoctor(Doctor treatingDoctor) { 
        this.treatingDoctor = treatingDoctor; 
    }
    Doctor getTreatingDoctor() { 
        return treatingDoctor; 
    }

    void setDaysToStay(int daysToStay) { 
        this.daysToStay = daysToStay; 
    }
    int getDaysToStay() { 
        return daysToStay; 
    }
}

class TeamMember {
    private String name;
    private String id;
    private String gender;
    private String dateJoined;
    private static final int MAX_WORKING_HOURS = 12;

    TeamMember(String name, String id, String gender, String dateJoined) {
        this.name = name;
        this.id = id;
        this.gender = gender;
        this.dateJoined = dateJoined;
    }

    void setName(String name) { 
        this.name = name; 
    }
    String getName() { 
        return name; 
    }

    void setId(String id) { 
        this.id = id; 
    }
    String getId() { 
        return id; 
    }

    void setGender(String gender) { 
        this.gender = gender; 
    }
    String getGender() { 
        return gender; 
    }

    void setDateJoined(String dateJoined) { 
        this.dateJoined = dateJoined; 
    }
    String getDateJoined() { 
        return dateJoined; 
    }

    static int getMaxWorkingHours() { 
        return MAX_WORKING_HOURS; 
    }
}

class Nurse extends TeamMember {
    Nurse(String name, String id, String gender, String dateJoined) {
        super(name, id, gender, dateJoined);
    }
}

class Doctor extends TeamMember {
    private String specialty;

    Doctor(String name, String id, String gender, String dateJoined, String specialty) {
        super(name, id, gender, dateJoined);
        this.specialty = specialty;
    }

    void setSpecialty(String specialty) { 
        this.specialty = specialty; 
    }
    String getSpecialty() { 
        return specialty; 
    }

    void checkPatientReport(HospitalPatient patient) {
        System.out.println("Dr. " + getName() + " checking report of " + patient.getName()
                         + ": " + patient.getReport());
    }

    void treatPatient(HospitalPatient patient) {
        System.out.println("Dr. " + getName() + " is treating patient " + patient.getName());
    }
}

class SeniorDoctor extends Doctor {
    private ArrayList<HospitalPatient> patients;

    SeniorDoctor(String name, String id, String gender, String dateJoined, String specialty) {
        super(name, id, gender, dateJoined, specialty);
        this.patients = new ArrayList<>();
    }

    ArrayList<HospitalPatient> getPatients() { 
        return patients; 
    }

    void addPatient(HospitalPatient patient) {
        patients.add(patient);
        patient.setTreatingDoctor(this);
    }

    void removePatient(HospitalPatient patient) {
        patients.remove(patient);
    }

    void treatPatient(HospitalPatient patient) {
        System.out.println("Senior Doctor " + getName() + " is performing a detailed examination "
                         + "and prescribing treatment for patient " + patient.getName());
    }
}

class Surgeon extends Doctor {
    private ArrayList<HospitalPatient> patients;

    Surgeon(String name, String id, String gender, String dateJoined, String specialty) {
        super(name, id, gender, dateJoined, specialty);
        this.patients = new ArrayList<>();
    }

    ArrayList<HospitalPatient> getPatients() { 
        return patients; 
    }

    void addPatient(HospitalPatient patient) {
        patients.add(patient);
        patient.setTreatingDoctor(this);
    }

    void removePatient(HospitalPatient patient) {
        patients.remove(patient);
    }

    void treatPatient(HospitalPatient patient) {
        System.out.println("Surgeon " + getName() + " is performing surgery on patient "
                         + patient.getName());
    }
}

class Intern extends Doctor {
    private SeniorDoctor supervisor;

    Intern(String name, String id, String gender, String dateJoined,
           String specialty, SeniorDoctor supervisor) {
        super(name, id, gender, dateJoined, specialty);
        this.supervisor = supervisor;
    }

    void setSupervisor(SeniorDoctor supervisor) { 
        this.supervisor = supervisor; 
    }
    SeniorDoctor getSupervisor() { 
        return supervisor; 
    }

    void treatPatient(HospitalPatient patient) {
        System.out.println("Intern " + getName() + " is treating patient " + patient.getName()
                         + " under supervision of Dr. " + supervisor.getName());
    }
}

class Department {
    private String name;
    private ArrayList<TeamMember> staff;

    Department(String name) {
        this.name = name;
        this.staff = new ArrayList<>();
    }

    void setName(String name) { 
        this.name = name; 
    }
    String getName() { 
        return name; 
    }

    ArrayList<TeamMember> getStaff() { 
        return staff; 
    }

    void addTeamMember(TeamMember member) {
        staff.add(member);
    }

    void removeTeamMember(TeamMember member) {
        staff.remove(member);
    }
}

class Hospital {
    private String name;
    private String address;
    private ArrayList<HospitalPatient> patients;
    private ArrayList<Department> departments;

    Hospital(String name, String address) {
        this.name = name;
        this.address = address;
        this.patients = new ArrayList<>();
        this.departments = new ArrayList<>();
    }

    void setName(String name) { 
        this.name = name; 
    }
    String getName() { 
        return name; 
    }

    void setAddress(String address) { 
        this.address = address; 
    }
    String getAddress() { 
        return address; 
    }

    ArrayList<HospitalPatient> getPatients() { 
        return patients; 
    }

    ArrayList<Department> getDepartments() { 
        return departments; 
    }

    void addPatient(HospitalPatient patient) {
        patients.add(patient);
    }

    void removePatient(HospitalPatient patient) {
        patients.remove(patient);
    }

    void addDepartment(Department dept) {
        departments.add(dept);
    }
}

public class Task2Lab9 {
    public static void main(String args[]) {
        Hospital hospital = new Hospital("City General Hospital", "123 Main Street, Islamabad");

        Department cardiology = new Department("Cardiology");
        Department pediatrics = new Department("Pediatrics");
        hospital.addDepartment(cardiology);
        hospital.addDepartment(pediatrics);

        SeniorDoctor drAhmed = new SeniorDoctor("Ahmed Khan", "D001", "Male",
                "2020-01-15", "Cardiology");
        SeniorDoctor drFatima = new SeniorDoctor("Fatima Ali", "D002", "Female",
                "2018-06-10", "Pediatrics");
        Surgeon drSarah = new Surgeon("Sarah Malik", "D003", "Female",
                "2015-03-20", "Cardiac Surgery");
        Intern drOmar = new Intern("Omar Raza", "D004", "Male",
                "2024-09-01", "Cardiology", drAhmed);
        Nurse nurseAyesha = new Nurse("Ayesha Noor", "N001", "Female", "2021-04-05");
        Nurse nurseKamran = new Nurse("Kamran Iqbal", "N002", "Male", "2022-07-12");

        cardiology.addTeamMember(drAhmed);
        cardiology.addTeamMember(drSarah);
        cardiology.addTeamMember(drOmar);
        cardiology.addTeamMember(nurseAyesha);
        pediatrics.addTeamMember(drFatima);
        pediatrics.addTeamMember(nurseKamran);

        HospitalPatient patient1 = new HospitalPatient("Ali Hassan", "1985-04-12",
                "Male", "2026-04-01", "Diagnosed with coronary artery disease", null, 10);
        HospitalPatient patient2 = new HospitalPatient("Zainab Bibi", "2000-08-25",
                "Female", "2026-03-20", "Diagnosed with congenital heart defect requiring surgery", null, 14);
        HospitalPatient patient3 = new HospitalPatient("Hassan Tariq", "2010-12-03",
                "Male", "2026-04-05", "Diagnosed with mild cardiac arrhythmia", null, 5);

        hospital.addPatient(patient1);
        hospital.addPatient(patient2);
        hospital.addPatient(patient3);

        drAhmed.addPatient(patient1);
        drSarah.addPatient(patient2);
        drAhmed.addPatient(patient3);

        System.out.println("Hospital: " + hospital.getName() + ", " + hospital.getAddress());
        System.out.println("Departments: " + cardiology.getName() + ", " + pediatrics.getName());
        System.out.println("Max working hours: " + TeamMember.getMaxWorkingHours());
        System.out.println();

        System.out.println("Cardiology staff:");
        int i = 0;
        while(i < cardiology.getStaff().size()) {
            TeamMember m = cardiology.getStaff().get(i);
            System.out.println(m.getName() + ", " + m.getId() + ", " + m.getGender()
                             + ", " + m.getDateJoined());
            i++;
        }
        System.out.println();

        System.out.println("Pediatrics staff:");
        i = 0;
        while(i < pediatrics.getStaff().size()) {
            TeamMember m = pediatrics.getStaff().get(i);
            System.out.println(m.getName() + ", " + m.getId() + ", " + m.getGender()
                             + ", " + m.getDateJoined());
            i++;
        }
        System.out.println();

        System.out.println("Patients:");
        i = 0;
        while(i < hospital.getPatients().size()) {
            HospitalPatient p = hospital.getPatients().get(i);
            String docName = p.getTreatingDoctor() != null ? p.getTreatingDoctor().getName() : "None";
            System.out.println(p.getName() + ", " + p.getBirthDate() + ", " + p.getGender()
                             + ", " + p.getDateAccepted() + ", Doctor: " + docName
                             + ", Days: " + p.getDaysToStay());
            i++;
        }
        System.out.println();

        Doctor doctors[] = { drAhmed, drSarah, drOmar };
        HospitalPatient pts[] = { patient1, patient2, patient3 };

        i = 0;
        while(i < doctors.length) {
            doctors[i].treatPatient(pts[i]);
            i++;
        }
        System.out.println();

        drAhmed.checkPatientReport(patient1);
        drSarah.checkPatientReport(patient2);
        drOmar.checkPatientReport(patient3);
        System.out.println();

        System.out.println("Patient1 name: " + patient1.getName());
        patient1.setName("Ali Hassan (Updated)");
        System.out.println("Patient1 updated name: " + patient1.getName());
        System.out.println("Patient1 days: " + patient1.getDaysToStay());
        patient1.setDaysToStay(12);
        System.out.println("Patient1 updated days: " + patient1.getDaysToStay());
        System.out.println("Dr Ahmed specialty: " + drAhmed.getSpecialty());
        drAhmed.setSpecialty("Interventional Cardiology");
        System.out.println("Dr Ahmed updated specialty: " + drAhmed.getSpecialty());
        System.out.println("Intern Omar supervisor: " + drOmar.getSupervisor().getName());
        System.out.println();

        cardiology.removeTeamMember(nurseAyesha);
        System.out.println("Removed " + nurseAyesha.getName() + " from cardiology");
        hospital.removePatient(patient3);
        drAhmed.removePatient(patient3);
        System.out.println("Removed patient " + patient3.getName());
        System.out.println();

        System.out.println("Cardiology staff after removal:");
        i = 0;
        while(i < cardiology.getStaff().size()) {
            System.out.println(cardiology.getStaff().get(i).getName());
            i++;
        }
        System.out.println();

        System.out.println("Patients after removal:");
        i = 0;
        while(i < hospital.getPatients().size()) {
            System.out.println(hospital.getPatients().get(i).getName());
            i++;
        }
        System.out.println();

        System.out.println("Dr Ahmed patients:");
        i = 0;
        while(i < drAhmed.getPatients().size()) {
            System.out.println(drAhmed.getPatients().get(i).getName());
            i++;
        }
        System.out.println("Dr Sarah patients:");
        i = 0;
        while(i < drSarah.getPatients().size()) {
            System.out.println(drSarah.getPatients().get(i).getName());
            i++;
        }
    }
}
