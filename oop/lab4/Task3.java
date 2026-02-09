import java.util.Scanner;

// task 3 - find the highest score
public class Task3 
{
    public static void main(String[] args) 
    {
        Scanner sc = new Scanner(System.in);
        
        System.out.print("Enter number of students: ");
        int n = sc.nextInt();
        
        if(n <= 0) {
            System.out.println("Invalid number of students!");
            sc.close();
            return;
        }
        
        String[] studentNames = new String[n];
        int[] studentScores = new int[n];
        
        int i = 0;
        while(i < n) {
            System.out.print("Student " + (i+1) + " name: ");
            studentNames[i] = sc.next();
            System.out.print("Student " + (i+1) + " score: ");
            studentScores[i] = sc.nextInt();
            i++;
        }
        
        String topStudent = studentNames[0];
        int topScore = studentScores[0];
        
        for(int j = 1; j < n; j++) {
            if(studentScores[j] > topScore) {
                topScore = studentScores[j];
                topStudent = studentNames[j];
            }
        }
        
        System.out.println("Student with highest score: " + topStudent);
        System.out.println("Score: " + topScore);
        
        sc.close();
    }
}
