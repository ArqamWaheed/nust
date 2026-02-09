public class Task2 {
    
    public static void main(String[] args) {
        double currentTuition = 10000.0;
        double rate = 0.06;
        int year = 0;
        
        // calculate tuition after 10 years
        double tuitionYear10 = currentTuition;
        while(year < 10) {
            tuitionYear10 = tuitionYear10 * (1 + rate);
            year++;
        }
        
        System.out.println("Tuition in 10 years: $" + String.format("%.2f", tuitionYear10));
        
        // calculate 4 years cost after 10th year
        double total = 0.0;
        double yearlyTuition = tuitionYear10;
        for(int i = 1; i <= 4; i++) {
            yearlyTuition = yearlyTuition * (1 + rate);
            total = total + yearlyTuition;
        }
        
        System.out.println("Total cost for 4 years after year 10: $" + String.format("%.2f", total));
    }
}
