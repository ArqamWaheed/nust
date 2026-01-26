public class Zeller {
    public static void main(String[] args) {
        int day = 15;
        int month = 8;
        int year = 2023;

        int originalMonth = month;
        int originalYear = year;

        if (month == 1 || month == 2) {
            month += 12;
            year -= 1;
        }

        int q = day;
        int m = month;
        int k = year % 100;
        int j = year / 100;

        int h = (q + (26 * (m + 1)) / 10 + k + k/4 + j/4 + 5*j) % 7;

        String dayName;
        if (h == 0) dayName = "Saturday";
        else if (h == 1) dayName = "Sunday";
        else if (h == 2) dayName = "Monday";
        else if (h == 3) dayName = "Tuesday";
        else if (h == 4) dayName = "Wednesday";
        else if (h == 5) dayName = "Thursday";
        else dayName = "Friday";

        System.out.println("Given Date: " + day + " / " + originalMonth + " / " + originalYear);
        System.out.println("Day of the Week: " + dayName);
    }
}
