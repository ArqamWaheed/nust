import java.sql.*;
import java.util.Scanner;

public class IssueApp {

    static final String URL  = "jdbc:mysql://localhost:3306/issue_db";
    static final String USER = "root";
    static final String PASS = "root";

    public static void main(String[] args) {
        try (Connection con = DriverManager.getConnection(URL, USER, PASS);
             Scanner sc = new Scanner(System.in)) {

            System.out.println("=============================================");
            System.out.println("  Issue Tracker Database Connected Successfully!");
            System.out.println("=============================================");

            boolean running = true;
            while (running) {
                printMainMenu();
                String choice = sc.nextLine().trim();
                switch (choice) {
                    case "1": registerUser(con, sc);       break;
                    case "2": createIssue(con, sc);        break;
                    case "3": assignIssue(con, sc);        break;
                    case "4": viewIssuesWithStaff(con);    break;
                    case "5": updateIssueStatus(con, sc);  break;
                    case "6": deleteIssue(con, sc);        break;
                    case "7": searchIssues(con, sc);       break;
                    case "8": running = false;             break;
                    default : System.out.println("Invalid option.");
                }
            }
            System.out.println("Goodbye.");
        } catch (SQLException e) {
            System.out.println("Database error: " + e.getMessage());
        }
    }

    static void printMainMenu() {
        System.out.println();
        System.out.println("============ ISSUE MAIN MENU ============");
        System.out.println(" 1. Register User");
        System.out.println(" 2. Create Issue");
        System.out.println(" 3. Assign Issue");
        System.out.println(" 4. View Issues with Staff");
        System.out.println(" 5. Update Issue Status");
        System.out.println(" 6. Delete Issue");
        System.out.println(" 7. Search Issues");
        System.out.println(" 8. Exit");
        System.out.print("Select option: ");
    }

    static void registerUser(Connection con, Scanner sc) {
        try {
            System.out.print("Enter User ID (number): ");
            int id = Integer.parseInt(sc.nextLine().trim());
            System.out.print("Enter Name: ");
            String name = sc.nextLine().trim();
            System.out.print("Enter Email: ");
            String email = sc.nextLine().trim();

            if (email.isEmpty()) {
                System.out.println("Email cannot be empty.");
                return;
            }

            String sql = "INSERT INTO User (user_id, name, email) VALUES (?, ?, ?)";
            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, id);
                ps.setString(2, name);
                ps.setString(3, email);
                int n = ps.executeUpdate();
                System.out.println(n + " user(s) registered successfully.");
            }
        } catch (NumberFormatException e) {
            System.out.println("Invalid number.");
        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void createIssue(Connection con, Scanner sc) {
        try {
            System.out.print("Enter User ID (must exist): ");
            int uid = Integer.parseInt(sc.nextLine().trim());
            System.out.print("Enter Title: ");
            String title = sc.nextLine().trim();
            System.out.print("Enter Description: ");
            String desc = sc.nextLine().trim();

            String sql = "INSERT INTO Issue (title, description, status, user_id) VALUES (?, ?, 'Pending', ?)";
            try (PreparedStatement ps = con.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
                ps.setString(1, title);
                ps.setString(2, desc);
                ps.setInt(3, uid);
                ps.executeUpdate();
                try (ResultSet rs = ps.getGeneratedKeys()) {
                    if (rs.next()) {
                        System.out.println("Issue created with ID " + rs.getInt(1) + " (status = Pending).");
                    }
                }
            }
        } catch (NumberFormatException e) {
            System.out.println("Invalid number.");
        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void assignIssue(Connection con, Scanner sc) {
        try {
            System.out.println();
            System.out.println("--- Issues ---");
            try (Statement st = con.createStatement();
                 ResultSet rs = st.executeQuery("SELECT issue_id, title, status FROM Issue")) {
                System.out.printf("%-4s  %-30s  %s%n", "ID", "Title", "Status");
                System.out.println("---------------------------------------------------");
                while (rs.next()) {
                    System.out.printf("%-4d  %-30s  %s%n",
                        rs.getInt(1), rs.getString(2), rs.getString(3));
                }
            }

            System.out.println();
            System.out.println("--- Staff ---");
            try (Statement st = con.createStatement();
                 ResultSet rs = st.executeQuery("SELECT staff_id, name, role FROM Staff")) {
                System.out.printf("%-4s  %-15s  %s%n", "ID", "Name", "Role");
                System.out.println("---------------------------------------------");
                while (rs.next()) {
                    System.out.printf("%-4d  %-15s  %s%n",
                        rs.getInt(1), rs.getString(2), rs.getString(3));
                }
            }

            System.out.print("Enter issue_id: ");
            int iid = Integer.parseInt(sc.nextLine().trim());
            System.out.print("Enter staff_id: ");
            int sid = Integer.parseInt(sc.nextLine().trim());

            String check = "SELECT 1 FROM Assignment WHERE issue_id = ?";
            try (PreparedStatement ps = con.prepareStatement(check)) {
                ps.setInt(1, iid);
                try (ResultSet rs = ps.executeQuery()) {
                    if (rs.next()) {
                        System.out.println("This issue is already assigned. Duplicate not allowed.");
                        return;
                    }
                }
            }

            String sql = "INSERT INTO Assignment (issue_id, staff_id) VALUES (?, ?)";
            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, iid);
                ps.setInt(2, sid);
                ps.executeUpdate();
                System.out.println("Issue " + iid + " assigned to staff " + sid + ".");
            }
        } catch (NumberFormatException e) {
            System.out.println("Invalid number.");
        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void viewIssuesWithStaff(Connection con) {
        String sql =
            "SELECT i.issue_id, i.title, i.status, COALESCE(s.name, 'Unassigned') AS staff " +
            "FROM Issue i " +
            "LEFT JOIN Assignment a ON i.issue_id = a.issue_id " +
            "LEFT JOIN Staff s ON a.staff_id = s.staff_id " +
            "ORDER BY i.issue_id";
        try (Statement st = con.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            System.out.println();
            System.out.println("--- ISSUES WITH STAFF ---");
            System.out.printf("%-4s  %-28s  %-12s  %s%n", "ID", "Title", "Status", "Staff");
            System.out.println("------------------------------------------------------------------");
            while (rs.next()) {
                System.out.printf("%-4d  %-28s  %-12s  %s%n",
                    rs.getInt(1), rs.getString(2), rs.getString(3), rs.getString(4));
            }
        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void updateIssueStatus(Connection con, Scanner sc) {
        try {
            System.out.print("Enter issue_id to update: ");
            int iid = Integer.parseInt(sc.nextLine().trim());

            String cur = null;
            try (PreparedStatement ps = con.prepareStatement("SELECT status FROM Issue WHERE issue_id = ?")) {
                ps.setInt(1, iid);
                try (ResultSet rs = ps.executeQuery()) {
                    if (!rs.next()) {
                        System.out.println("Issue not found.");
                        return;
                    }
                    cur = rs.getString(1);
                }
            }

            String next;
            switch (cur) {
                case "Pending":     next = "In Progress"; break;
                case "In Progress": next = "Resolved";    break;
                default: System.out.println("Issue is already Resolved."); return;
            }

            try (PreparedStatement ps = con.prepareStatement("UPDATE Issue SET status = ? WHERE issue_id = ?")) {
                ps.setString(1, next);
                ps.setInt(2, iid);
                int n = ps.executeUpdate();
                if (n > 0) System.out.println("Status updated: " + cur + " -> " + next);
            }
        } catch (NumberFormatException e) {
            System.out.println("Invalid number.");
        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void deleteIssue(Connection con, Scanner sc) {
        try {
            System.out.print("Enter issue_id to delete: ");
            int iid = Integer.parseInt(sc.nextLine().trim());

            try (PreparedStatement ps = con.prepareStatement("SELECT 1 FROM Assignment WHERE issue_id = ?")) {
                ps.setInt(1, iid);
                try (ResultSet rs = ps.executeQuery()) {
                    if (rs.next()) {
                        System.out.println("Cannot delete assigned issue.");
                        return;
                    }
                }
            }

            try (PreparedStatement ps = con.prepareStatement("DELETE FROM Issue WHERE issue_id = ?")) {
                ps.setInt(1, iid);
                int n = ps.executeUpdate();
                if (n == 0) System.out.println("Issue not found.");
                else        System.out.println("Issue deleted.");
            }
        } catch (NumberFormatException e) {
            System.out.println("Invalid number.");
        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void searchIssues(Connection con, Scanner sc) {
        System.out.print("Search by (1) Status or (2) Issue ID: ");
        String mode = sc.nextLine().trim();
        try {
            if (mode.equals("1")) {
                System.out.print("Enter status: ");
                String st = sc.nextLine().trim();
                try (PreparedStatement ps = con.prepareStatement(
                        "SELECT issue_id, title, status FROM Issue WHERE status = ?")) {
                    ps.setString(1, st);
                    try (ResultSet rs = ps.executeQuery()) {
                        while (rs.next()) {
                            System.out.printf("%d  %s  [%s]%n",
                                rs.getInt(1), rs.getString(2), rs.getString(3));
                        }
                    }
                }
            } else if (mode.equals("2")) {
                System.out.print("Enter issue_id: ");
                int iid = Integer.parseInt(sc.nextLine().trim());
                try (PreparedStatement ps = con.prepareStatement(
                        "SELECT issue_id, title, status FROM Issue WHERE issue_id = ?")) {
                    ps.setInt(1, iid);
                    try (ResultSet rs = ps.executeQuery()) {
                        if (rs.next()) {
                            System.out.printf("%d  %s  [%s]%n",
                                rs.getInt(1), rs.getString(2), rs.getString(3));
                        } else {
                            System.out.println("No issue with that ID.");
                        }
                    }
                }
            } else {
                System.out.println("Invalid mode.");
            }
        } catch (NumberFormatException e) {
            System.out.println("Invalid number.");
        } catch (SQLException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
