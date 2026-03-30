class Date {
    int m;
    int d;
    int y;

    Date(int month, int day, int year) {
        m = month;
        d = day;
        y = year;
    }

    void setM(int month) { 
        m = month;
    }

    int getM() {
         return m;
     }

    void setD(int day) {
         d = day;
     }
    int getD() {
         return d; 
    }

    void setY(int year) {
         y = year;
    }
    int getY() {
         return y; 
    }

    void showDate() {
        System.out.println(m + "/" + d + "/" + y);
    }
}

public class Task2 {
    public static void main(String args[]) {
        Date d1 = new Date(3, 15, 2025);
        Date d2 = new Date(8, 20, 2024);

        System.out.print("First Date: ");
        d1.showDate();

        System.out.print("Second Date: ");
        d2.showDate();

        d1.setM(11);
        d1.setD(30);
        d1.setY(2023);

        System.out.print("Updated First Date: ");
        d1.showDate();
    }
}
