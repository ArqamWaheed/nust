class Student {
    String studentId;
    String name;
    String department;

    Student(String studentId, String name, String department) {
        this.studentId = studentId;
        this.name = name;
        this.department = department;
    }

    void setStudentId(String studentId) { 
        this.studentId = studentId; 
    }
    String getStudentId() { 
        return studentId; 
    }

    void setName(String name) { 
        this.name = name; 
    }
    String getName() { 
        return name; 
    }

    void setDepartment(String department) { 
        this.department = department; 
    }
    String getDepartment() { 
        return department; 
    }

    double computeFinalScore() {
        return 0.0;
    }

    String categorize() {
        double score = computeFinalScore();
        if(score >= 85)
            return "Excellent";
        else if(score >= 70)
            return "Good";
        else if(score >= 50)
            return "Needs Improvement";
        else
            return "Fail";
    }

    String getEvaluationType() {
        return "General";
    }
}

class ExamStudent extends Student {
    double midterm;
    double finalExam;

    ExamStudent(String studentId, String name, String department, double midterm, double finalExam) {
        super(studentId, name, department);
        this.midterm = midterm;
        this.finalExam = finalExam;
    }

    void setMidterm(double midterm) { 
        this.midterm = midterm; 
    }
    double getMidterm() { 
        return midterm; 
    }

    void setFinalExam(double finalExam) { 
        this.finalExam = finalExam; 
    }
    double getFinalExam() { 
        return finalExam; 
    }

    double computeFinalScore() {
        return midterm * 0.4 + finalExam * 0.6;
    }

    String getEvaluationType() {
        return "Exam-Based";
    }
}

class ProjectStudent extends Student {
    double quizAvg;
    double projectScore;
    double presentationScore;

    ProjectStudent(String studentId, String name, String department, 
                   double quizAvg, double projectScore, double presentationScore) {
        super(studentId, name, department);
        this.quizAvg = quizAvg;
        this.projectScore = projectScore;
        this.presentationScore = presentationScore;
    }

    void setQuizAvg(double quizAvg) { 
        this.quizAvg = quizAvg; 
    }
    double getQuizAvg() { 
        return quizAvg; 
    }

    void setProjectScore(double projectScore) { 
        this.projectScore = projectScore; 
    }
    double getProjectScore() { 
        return projectScore; 
    }

    void setPresentationScore(double presentationScore) { 
        this.presentationScore = presentationScore; 
    }
    double getPresentationScore() { 
        return presentationScore; 
    }

    double computeFinalScore() {
        return quizAvg * 0.3 + projectScore * 0.4 + presentationScore * 0.3;
    }

    String getEvaluationType() {
        return "Project-Based";
    }
}

class AttendanceStudent extends ExamStudent {
    double attendancePercent;

    AttendanceStudent(String studentId, String name, String department, 
                      double midterm, double finalExam, double attendancePercent) {
        super(studentId, name, department, midterm, finalExam);
        this.attendancePercent = attendancePercent;
    }

    void setAttendancePercent(double attendancePercent) { 
        this.attendancePercent = attendancePercent; 
    }
    double getAttendancePercent() { 
        return attendancePercent; 
    }

    double computeFinalScore() {
        double examScore = midterm * 0.4 + finalExam * 0.6;
        return examScore * 0.85 + attendancePercent * 0.15;
    }

    String getEvaluationType() {
        return "Attendance-Weighted";
    }
}

class GradingProcessor {
    Student studentList[];
    int totalStudents;

    GradingProcessor(Student studentList[], int totalStudents) {
        this.studentList = studentList;
        this.totalStudents = totalStudents;
    }

    Student findTopPerformer() {
        Student top = studentList[0];
        int idx = 1;
        while(idx < totalStudents) {
            if(studentList[idx].computeFinalScore() > top.computeFinalScore())
                top = studentList[idx];
            idx++;
        }
        return top;
    }

    void evaluateSingleStudent(int index) {
        Student s = studentList[index];
        System.out.println("Student: " + s.getName() + ", Type: " + s.getEvaluationType() 
                           + ", Score: " + s.computeFinalScore() 
                           + ", Category: " + s.categorize());
    }

    void showReport() {
        int idx = 0;
        while(idx < totalStudents) {
            System.out.println(studentList[idx].getStudentId() + ", " 
                               + studentList[idx].getName() + ", " 
                               + studentList[idx].getDepartment() + ", "
                               + studentList[idx].getEvaluationType() + ", Score: " 
                               + studentList[idx].computeFinalScore() + ", " 
                               + studentList[idx].categorize());
            idx++;
        }
        Student top = findTopPerformer();
        System.out.println("Top Performer: " + top.getName() + ", Score: " + top.computeFinalScore());
    }
}

public class Task3Lab8 {
    public static void main(String args[]) {
        Student studentList[] = new Student[5];
        studentList[0] = new ExamStudent("S001", "Ali Raza", "CS", 78, 88);
        studentList[1] = new ProjectStudent("S002", "Fatima Noor", "SE", 80, 90, 85);
        studentList[2] = new AttendanceStudent("S003", "Hamza Iqbal", "EE", 70, 75, 92);
        studentList[3] = new ExamStudent("S004", "Zainab Malik", "CS", 55, 60);
        studentList[4] = new ProjectStudent("S005", "Omar Farooq", "SE", 90, 95, 88);

        GradingProcessor processor = new GradingProcessor(studentList, 5);
        processor.showReport();

        System.out.println();
        processor.evaluateSingleStudent(2);
    }
}
