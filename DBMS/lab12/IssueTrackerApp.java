import java.sql.*;
import java.util.Scanner;

/**
 * Lab 12 – Advanced JDBC
 * Issue Tracker (User / Issue / Staff / Assignment)
 *
 * - try-with-resources for Connection / PreparedStatement / ResultSet / Scanner
 * - try/catch around every SQL call (errors print and return to menu)
 * - PreparedStatement everywhere (no SQL injection)
 */
public class IssueTrackerApp {

    static final String URL  = "jdbc:mysql://localhost:3306/IssueTrackerDB";
    static final String USER = "root";
    static final String PASS = "root";

    public static void main(String[] args) {
        try (Connection con = DriverManager.getConnection(URL, USER, PASS);
             Scanner sc = new Scanner(System.in)) {

            System.out.println("Connected to MySQL (IssueTrackerDB) successfully.");

            while (true) {
                System.out.println();
                System.out.println("===== Issue Tracker =====");
                System.out.println("1. Register User");
                System.out.println("2. Create Issue");
                System.out.println("3. Assign Issue");
                System.out.println("4. View Issues with Staff");
                System.out.println("5. Update Issue Status");
                System.out.println("6. Delete Issue");
                System.out.println("7. Search Issues");
                System.out.println("8. Exit");
                System.out.print("Choice: ");
                String choice = sc.nextLine().trim();

                switch (choice) {
                    case "1": registerUser(con, sc);     break;
                    case "2": createIssue(con, sc);      break;
                    case "3": assignIssue(con, sc);      break;
                    case "4": viewIssuesWithStaff(con);  break;
                    case "5": updateIssueStatus(con, sc);break;
                    case "6": deleteIssue(con, sc);      break;
                    case "7": searchIssues(con, sc);     break;
                    case "8": System.out.println("Goodbye."); return;
                    default : System.out.println("Invalid choice.");
                }
            }
        } catch (SQLException e) {
            System.out.println("Connection failed: " + e.getMessage());
        }
    }

    // ---------- 1. Register User ----------
    static void registerUser(Connection con, Scanner sc) {
        System.out.print("Name: ");
        String name = sc.nextLine().trim();
        System.out.print("Email: ");
        String email = sc.nextLine().trim();

        if (email.isEmpty()) {
            System.out.println("Error: email cannot be empty.");
            return;
        }
        String sql = "INSERT INTO User(name, email) VALUES(?,?)";
        try (PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setString(1, name);
            ps.setString(2, email);
            int n = ps.executeUpdate();
            System.out.println(n + " user(s) registered.");
        } catch (SQLException e) {
            System.out.println("Insert failed: " + e.getMessage());
        }
    }

    // ---------- 2. Create Issue ----------
    static void createIssue(Connection con, Scanner sc) {
        System.out.print("Title: ");
        String title = sc.nextLine().trim();
        System.out.print("Description: ");
        String desc = sc.nextLine().trim();

        String sql = "INSERT INTO Issue(title, description, status) VALUES(?,?, 'Pending')";
        try (PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setString(1, title);
            ps.setString(2, desc);
            int n = ps.executeUpdate();
            System.out.println(n + " issue(s) created with status = Pending.");
        } catch (SQLException e) {
            System.out.println("Insert failed: " + e.getMessage());
        }
    }

    // ---------- 3. Assign Issue ----------
    static void assignIssue(Connection con, Scanner sc) {
        System.out.println("--- Issues ---");
        runReadQuery(con, "SELECT issue_id, title, status FROM Issue");
        System.out.println("--- Staff ---");
        runReadQuery(con, "SELECT staff_id, name, role FROM Staff");

        System.out.print("Issue ID: ");
        int issueId = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Staff ID: ");
        int staffId = Integer.parseInt(sc.nextLine().trim());

        String sql = "INSERT INTO Assignment(issue_id, staff_id) VALUES(?,?)";
        try (PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, issueId);
            ps.setInt(2, staffId);
            int n = ps.executeUpdate();
            System.out.println(n + " assignment(s) created.");
        } catch (SQLException e) {
            System.out.println("Assignment failed: " + e.getMessage());
        }
    }

    // ---------- 4. View Issues + Staff (JOIN) ----------
    static void viewIssuesWithStaff(Connection con) {
        String sql =
            "SELECT i.issue_id, i.title, i.status, " +
            "       COALESCE(s.name,'-- unassigned --') AS staff_name " +
            "FROM Issue i " +
            "LEFT JOIN Assignment a ON a.issue_id = i.issue_id " +
            "LEFT JOIN Staff s      ON s.staff_id = a.staff_id";
        try (PreparedStatement ps = con.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            System.out.println("IssueID\tTitle\t\t\tStatus\t\tStaff");
            while (rs.next()) {
                System.out.printf("%d\t%-22s\t%-10s\t%s%n",
                        rs.getInt("issue_id"),
                        rs.getString("title"),
                        rs.getString("status"),
                        rs.getString("staff_name"));
            }
        } catch (SQLException e) {
            System.out.println("Read failed: " + e.getMessage());
        }
    }

    // ---------- 5. Update Issue Status ----------
    static void updateIssueStatus(Connection con, Scanner sc) {
        System.out.print("Issue ID: ");
        int id = Integer.parseInt(sc.nextLine().trim());
        System.out.print("New status (Pending / In Progress / Resolved): ");
        String status = sc.nextLine().trim();

        String sql = "UPDATE Issue SET status = ? WHERE issue_id = ?";
        try (PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setString(1, status);
            ps.setInt(2, id);
            int n = ps.executeUpdate();
            if (n == 0) System.out.println("No issue with that ID.");
            else        System.out.println("Status updated for issue " + id + ".");
        } catch (SQLException e) {
            System.out.println("Update failed: " + e.getMessage());
        }
    }

    // ---------- 6. Delete Issue (controlled) ----------
    static void deleteIssue(Connection con, Scanner sc) {
        System.out.print("Issue ID: ");
        int id = Integer.parseInt(sc.nextLine().trim());

        // refuse if assigned
        String check = "SELECT COUNT(*) FROM Assignment WHERE issue_id = ?";
        try (PreparedStatement ps = con.prepareStatement(check)) {
            ps.setInt(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next() && rs.getInt(1) > 0) {
                    System.out.println("Cannot delete assigned issue.");
                    return;
                }
            }
        } catch (SQLException e) {
            System.out.println("Check failed: " + e.getMessage());
            return;
        }

        String sql = "DELETE FROM Issue WHERE issue_id = ?";
        try (PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, id);
            int n = ps.executeUpdate();
            if (n == 0) System.out.println("No issue with that ID.");
            else        System.out.println(n + " issue(s) deleted.");
        } catch (SQLException e) {
            System.out.println("Delete failed: " + e.getMessage());
        }
    }

    // ---------- 7. Search ----------
    static void searchIssues(Connection con, Scanner sc) {
        System.out.println("Search by: 1.Status  2.Issue ID");
        String mode = sc.nextLine().trim();

        if (mode.equals("1")) {
            System.out.print("Status: ");
            String st = sc.nextLine().trim();
            String sql = "SELECT issue_id, title, status FROM Issue WHERE status = ?";
            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setString(1, st);
                printIssueRs(ps);
            } catch (SQLException e) {
                System.out.println("Search failed: " + e.getMessage());
            }
        } else if (mode.equals("2")) {
            System.out.print("Issue ID: ");
            int id = Integer.parseInt(sc.nextLine().trim());
            String sql = "SELECT issue_id, title, status FROM Issue WHERE issue_id = ?";
            try (PreparedStatement ps = con.prepareStatement(sql)) {
                ps.setInt(1, id);
                printIssueRs(ps);
            } catch (SQLException e) {
                System.out.println("Search failed: " + e.getMessage());
            }
        } else {
            System.out.println("Invalid option.");
        }
    }

    // ---------- helpers ----------
    static void printIssueRs(PreparedStatement ps) throws SQLException {
        try (ResultSet rs = ps.executeQuery()) {
            System.out.println("IssueID\tTitle\t\t\tStatus");
            int count = 0;
            while (rs.next()) {
                count++;
                System.out.printf("%d\t%-22s\t%s%n",
                        rs.getInt(1), rs.getString(2), rs.getString(3));
            }
            if (count == 0) System.out.println("(no rows)");
        }
    }

    static void runReadQuery(Connection con, String sql) {
        try (PreparedStatement ps = con.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            ResultSetMetaData md = rs.getMetaData();
            int cols = md.getColumnCount();
            for (int i = 1; i <= cols; i++)
                System.out.print(md.getColumnLabel(i) + (i < cols ? "\t" : "\n"));
            while (rs.next()) {
                for (int i = 1; i <= cols; i++)
                    System.out.print(rs.getString(i) + (i < cols ? "\t" : "\n"));
            }
        } catch (SQLException e) {
            System.out.println("Read failed: " + e.getMessage());
        }
    }
}
