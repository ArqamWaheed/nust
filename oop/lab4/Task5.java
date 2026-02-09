// task 5 - all combinations for picking two numbers from 1 to 7
public class Task5 
{
    public static void main(String[] args) 
    {
        System.out.println("All combinations pick(2 from 1-7):");
        
        int counter = 0;
        int first = 1;
        
        while(first <= 7) {
            int second = first + 1;
            while(second <= 7) {
                System.out.println("(" + first + ", " + second + ")");
                counter++;
                second++;
            }
            first++;
        }
        
        System.out.println("Total number of combinations: " + counter);
    }
}
