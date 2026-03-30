class Student {
    String rollNo;
    String name;
    String dept;

    Student(String rollNo, String name, String dept) {
        this.rollNo = rollNo;
        this.name = name;
        this.dept = dept;
    }

    void setRollNo(String rollNo) { 
        this.rollNo = rollNo; 
    }
    String getRollNo() { 
        return rollNo; 
    }

    void setName(String name) { 
        this.name = name; 
    }
    String getName() { 
        return name; 
    }

    void setDept(String dept) { 
        this.dept = dept; 
    }
    String getDept() { 
        return dept; 
    }

    String evalType() {
        return "General";
    }

    double finalScore() {
        return 0.0;
    }

    String grade() {
        double s = finalScore();
        if(s >= 85)
            return "Excellent";
        else if(s >= 70)
            return "Good";
        else if(s >= 50)
            return "Needs Improvement";
        return "Fail";
    }
}

class ExamStudent extends Student {
    double mid;
    double fin;

    ExamStudent(String rollNo, String name, String dept, double mid, double fin) {
        super(rollNo, name, dept);
        this.mid = mid;
        this.fin = fin;
    }

    void setMid(double mid) { 
        this.mid = mid; 
    }
    double getMid() { 
        return mid; 
    }

    void setFin(double fin) { 
        this.fin = fin; 
    }
    double getFin() { 
        return fin; 
    }

    String evalType() {
        return "Exam-Only";
    }

    double finalScore() {
        return mid * 0.4 + fin * 0.6;
    }
}

class ProjectStudent extends Student {
    double quiz;
    double project;
    double presentation;

    ProjectStudent(String rollNo, String name, String dept, 
                   double quiz, double project, double presentation) {
        super(rollNo, name, dept);
        this.quiz = quiz;
        this.project = project;
        this.presentation = presentation;
    }

    void setQuiz(double quiz) { 
        this.quiz = quiz; 
    }
    double getQuiz() { 
        return quiz; 
    }

    void setProject(double project) { 
        this.project = project; 
    }
    double getProject() { 
        return project; 
    }

    void setPresentation(double presentation) { 
        this.presentation = presentation; 
    }
    double getPresentation() { 
        return presentation; 
    }

    String evalType() {
        return "Project-Based";
    }

    double finalScore() {
        return quiz * 0.3 + project * 0.4 + presentation * 0.3;
    }
}

class AttendanceStudent extends ExamStudent {
    double attendance;

    AttendanceStudent(String rollNo, String name, String dept, 
                      double mid, double fin, double attendance) {
        super(rollNo, name, dept, mid, fin);
        this.attendance = attendance;
    }

    void setAttendance(double attendance) { 
        this.attendance = attendance; 
    }
    double getAttendance() { 
        return attendance; 
    }

    String evalType() {
        return "Attendance-Adjusted";
    }

    double finalScore() {
        double exam = mid * 0.4 + fin * 0.6;
        return exam * 0.85 + attendance * 0.15;
    }
}

class ResultProcessor {
    Student students[];
    int size;

    ResultProcessor(Student students[], int size) {
        this.students = students;
        this.size = size;
    }

    Student topStudent() {
        Student best = students[0];
        int i = 1;
        while(i < size) {
            if(students[i].finalScore() > best.finalScore())
                best = students[i];
            i++;
        }
        return best;
    }

    void checkOne(int idx) {
        Student s = students[idx];
        System.out.println("Student: " + s.getName() + ", Eval: " + s.evalType() 
                           + ", Score: " + s.finalScore() + ", Grade: " + s.grade());
    }

    void report() {
        int i = 0;
        while(i < size) {
            System.out.println(students[i].getRollNo() + ", " + students[i].getName() 
                               + ", " + students[i].getDept() + ", " + students[i].evalType() 
                               + ", Score: " + students[i].finalScore() 
                               + ", " + students[i].grade());
            i++;
        }
        Student best = topStudent();
        System.out.println("Top: " + best.getName() + ", Score: " + best.finalScore());
    }
}

public class Task3Lab8 {
    public static void main(String args[]) {
        Student students[] = new Student[5];
        students[0] = new ProjectStudent("R01", "Taimoor Aslam", "SE", 88, 92, 80);
        students[1] = new ExamStudent("R02", "Saba Perveen", "CS", 72, 65);
        students[2] = new AttendanceStudent("R03", "Danish Nawaz", "EE", 68, 80, 95);
        students[3] = new ProjectStudent("R04", "Komal Shahzadi", "SE", 75, 85, 90);
        students[4] = new ExamStudent("R05", "Junaid Ashraf", "CS", 90, 88);

        ResultProcessor rp = new ResultProcessor(students, 5);
        rp.report();

        System.out.println();
        rp.checkOne(0);
    }
}
