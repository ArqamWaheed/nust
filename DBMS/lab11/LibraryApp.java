import java.sql.*;
import java.util.Scanner;

public class LibraryApp {

    private static final String URL  = "jdbc:mysql://localhost:3306/LibraryDB";
    private static final String USER = "labuser";
    private static final String PASS = "LabPass_123!";

    public static void main(String[] args) {
        try (Connection con = DriverManager.getConnection(URL, USER, PASS);
             Scanner sc = new Scanner(System.in)) {

            System.out.println("Connected to MySQL (LibraryDB) successfully.");

            while (true) {
                printMenu();
                int choice = readInt(sc);
                switch (choice) {
                    case 1: insertMenu(con, sc);     break;
                    case 2: viewMenu(con, sc);       break;
                    case 3: updateMenu(con, sc);     break;
                    case 4: deleteMenu(con, sc);     break;
                    case 5: viewJoinedData(con);     break;
                    case 6:
                        System.out.println("Goodbye.");
                        return;
                    default:
                        System.out.println("Invalid choice.");
                }
            }
        } catch (SQLException e) {
            System.err.println("Database connection failed: " + e.getMessage());
        }
    }

    private static void printMenu() {
        System.out.println("\n===== Library Management System =====");
        System.out.println("1. Insert Record");
        System.out.println("2. View Records");
        System.out.println("3. Update Record");
        System.out.println("4. Delete Record");
        System.out.println("5. View Joined Data (Loan + BookCopy + Book + Author + Member)");
        System.out.println("6. Exit");
        System.out.print("Choice: ");
    }

    // ---------- INSERT ----------
    private static void insertMenu(Connection con, Scanner sc) {
        System.out.println("Insert into: 1.Librarian 2.Member 3.BookAuthor 4.Book 5.BookCopy 6.Loan 7.Fee");
        int c = readInt(sc);
        try {
            switch (c) {
                case 1: {
                    System.out.print("LibrarianID: ");   int id = readInt(sc);
                    System.out.print("Name: ");          String n  = sc.nextLine();
                    System.out.print("Email: ");         String e  = sc.nextLine();
                    System.out.print("Phone: ");         String ph = sc.nextLine();
                    String sql = "INSERT INTO Librarian VALUES (?,?,?,?)";
                    try (PreparedStatement ps = con.prepareStatement(sql)) {
                        ps.setInt(1, id); ps.setString(2, n); ps.setString(3, e); ps.setString(4, ph);
                        System.out.println(ps.executeUpdate() + " row(s) inserted.");
                    }
                    break;
                }
                case 2: {
                    System.out.print("MemberID: ");                    int id = readInt(sc);
                    System.out.print("Name: ");                        String n = sc.nextLine();
                    System.out.print("Membership Date (YYYY-MM-DD): "); String d = sc.nextLine();
                    System.out.print("Status: ");                      String s = sc.nextLine();
                    String sql = "INSERT INTO Member VALUES (?,?,?,?)";
                    try (PreparedStatement ps = con.prepareStatement(sql)) {
                        ps.setInt(1, id); ps.setString(2, n);
                        ps.setDate(3, Date.valueOf(d)); ps.setString(4, s);
                        System.out.println(ps.executeUpdate() + " row(s) inserted.");
                    }
                    break;
                }
                case 3: {
                    System.out.print("AuthorID: ");   int id = readInt(sc);
                    System.out.print("AuthorName: "); String n = sc.nextLine();
                    String sql = "INSERT INTO BookAuthor VALUES (?,?)";
                    try (PreparedStatement ps = con.prepareStatement(sql)) {
                        ps.setInt(1, id); ps.setString(2, n);
                        System.out.println(ps.executeUpdate() + " row(s) inserted.");
                    }
                    break;
                }
                case 4: {
                    System.out.print("BookID: ");    int id = readInt(sc);
                    System.out.print("BookName: ");  String n = sc.nextLine();
                    System.out.print("AuthorID: ");  int a  = readInt(sc);
                    System.out.print("Category: ");  String cat = sc.nextLine();
                    String sql = "INSERT INTO Book VALUES (?,?,?,?)";
                    try (PreparedStatement ps = con.prepareStatement(sql)) {
                        ps.setInt(1, id); ps.setString(2, n); ps.setInt(3, a); ps.setString(4, cat);
                        System.out.println(ps.executeUpdate() + " row(s) inserted.");
                    }
                    break;
                }
                case 5: {
                    System.out.print("CopyID: "); int id = readInt(sc);
                    System.out.print("BookID: "); int b  = readInt(sc);
                    System.out.print("Status: "); String s = sc.nextLine();
                    String sql = "INSERT INTO BookCopy VALUES (?,?,?)";
                    try (PreparedStatement ps = con.prepareStatement(sql)) {
                        ps.setInt(1, id); ps.setInt(2, b); ps.setString(3, s);
                        System.out.println(ps.executeUpdate() + " row(s) inserted.");
                    }
                    break;
                }
                case 6: {
                    System.out.print("LoanID: ");                    int id = readInt(sc);
                    System.out.print("CopyID: ");                    int co = readInt(sc);
                    System.out.print("MemberID: ");                  int m  = readInt(sc);
                    System.out.print("Issue Date (YYYY-MM-DD): ");   String iss = sc.nextLine();
                    System.out.print("Due Date (YYYY-MM-DD): ");     String due = sc.nextLine();
                    System.out.print("Return Date (blank if none): "); String ret = sc.nextLine();
                    String sql = "INSERT INTO Loan VALUES (?,?,?,?,?,?)";
                    try (PreparedStatement ps = con.prepareStatement(sql)) {
                        ps.setInt(1, id); ps.setInt(2, co); ps.setInt(3, m);
                        ps.setDate(4, Date.valueOf(iss));
                        ps.setDate(5, Date.valueOf(due));
                        if (ret.isEmpty()) ps.setNull(6, Types.DATE);
                        else               ps.setDate(6, Date.valueOf(ret));
                        System.out.println(ps.executeUpdate() + " row(s) inserted.");
                    }
                    break;
                }
                case 7: {
                    System.out.print("PaymentID: "); int id = readInt(sc);
                    System.out.print("MemberID: ");  int m  = readInt(sc);
                    String sql = "INSERT INTO Fee VALUES (?,?)";
                    try (PreparedStatement ps = con.prepareStatement(sql)) {
                        ps.setInt(1, id); ps.setInt(2, m);
                        System.out.println(ps.executeUpdate() + " row(s) inserted.");
                    }
                    break;
                }
                default: System.out.println("Invalid.");
            }
        } catch (SQLException | IllegalArgumentException ex) {
            System.err.println("Insert failed: " + ex.getMessage());
        }
    }

    // ---------- READ ----------
    private static void viewMenu(Connection con, Scanner sc) {
        System.out.println("View: 1.Librarian 2.Member 3.BookAuthor 4.Book 5.BookCopy 6.Loan 7.Fee");
        int c = readInt(sc);
        String sql;
        switch (c) {
            case 1: sql = "SELECT * FROM Librarian";  break;
            case 2: sql = "SELECT * FROM Member";     break;
            case 3: sql = "SELECT * FROM BookAuthor"; break;
            case 4: sql = "SELECT * FROM Book";       break;
            case 5: sql = "SELECT * FROM BookCopy";   break;
            case 6: sql = "SELECT * FROM Loan";       break;
            case 7: sql = "SELECT * FROM Fee";        break;
            default: System.out.println("Invalid."); return;
        }
        try (Statement st = con.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            printResultSet(rs);
        } catch (SQLException e) {
            System.err.println("Query failed: " + e.getMessage());
        }
    }

    // ---------- UPDATE ----------
    private static void updateMenu(Connection con, Scanner sc) {
        System.out.println("Update: 1.Member status  2.Book category  3.BookCopy status  4.Loan return date");
        int c = readInt(sc);
        try {
            switch (c) {
                case 1: {
                    System.out.print("MemberID: ");   int id = readInt(sc);
                    System.out.print("New status: "); String s = sc.nextLine();
                    String sql = "UPDATE Member SET Status=? WHERE MemberID=?";
                    try (PreparedStatement ps = con.prepareStatement(sql)) {
                        ps.setString(1, s); ps.setInt(2, id);
                        System.out.println(ps.executeUpdate() + " row(s) updated.");
                    }
                    break;
                }
                case 2: {
                    System.out.print("BookID: ");       int id = readInt(sc);
                    System.out.print("New category: "); String cat = sc.nextLine();
                    String sql = "UPDATE Book SET Category=? WHERE BookID=?";
                    try (PreparedStatement ps = con.prepareStatement(sql)) {
                        ps.setString(1, cat); ps.setInt(2, id);
                        System.out.println(ps.executeUpdate() + " row(s) updated.");
                    }
                    break;
                }
                case 3: {
                    System.out.print("CopyID: ");     int id = readInt(sc);
                    System.out.print("New status: "); String s = sc.nextLine();
                    String sql = "UPDATE BookCopy SET Status=? WHERE CopyID=?";
                    try (PreparedStatement ps = con.prepareStatement(sql)) {
                        ps.setString(1, s); ps.setInt(2, id);
                        System.out.println(ps.executeUpdate() + " row(s) updated.");
                    }
                    break;
                }
                case 4: {
                    System.out.print("LoanID: ");                   int id = readInt(sc);
                    System.out.print("Return Date (YYYY-MM-DD): "); String d = sc.nextLine();
                    String sql = "UPDATE Loan SET Return_Date=? WHERE LoanID=?";
                    try (PreparedStatement ps = con.prepareStatement(sql)) {
                        ps.setDate(1, Date.valueOf(d)); ps.setInt(2, id);
                        System.out.println(ps.executeUpdate() + " row(s) updated.");
                    }
                    break;
                }
                default: System.out.println("Invalid.");
            }
        } catch (SQLException | IllegalArgumentException ex) {
            System.err.println("Update failed: " + ex.getMessage());
        }
    }

    // ---------- DELETE ----------
    private static void deleteMenu(Connection con, Scanner sc) {
        System.out.println("Delete from: 1.Librarian 2.Member 3.BookAuthor 4.Book 5.BookCopy 6.Loan 7.Fee");
        int c = readInt(sc);
        String sql, label;
        switch (c) {
            case 1: sql = "DELETE FROM Librarian  WHERE LibrarianID=?"; label = "LibrarianID"; break;
            case 2: sql = "DELETE FROM Member     WHERE MemberID=?";    label = "MemberID";    break;
            case 3: sql = "DELETE FROM BookAuthor WHERE AuthorID=?";    label = "AuthorID";    break;
            case 4: sql = "DELETE FROM Book       WHERE BookID=?";      label = "BookID";      break;
            case 5: sql = "DELETE FROM BookCopy   WHERE CopyID=?";      label = "CopyID";      break;
            case 6: sql = "DELETE FROM Loan       WHERE LoanID=?";      label = "LoanID";      break;
            case 7: sql = "DELETE FROM Fee        WHERE PaymentID=?";   label = "PaymentID";   break;
            default: System.out.println("Invalid."); return;
        }
        System.out.print(label + ": ");
        int id = readInt(sc);
        try (PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, id);
            System.out.println(ps.executeUpdate() + " row(s) deleted.");
        } catch (SQLException e) {
            System.err.println("Delete failed (referential integrity?): " + e.getMessage());
        }
    }

    // ---------- JOIN ----------
    private static void viewJoinedData(Connection con) {
        String sql =
            "SELECT l.LoanID, m.MemberName AS Member, b.BookName AS Book, " +
            "       a.AuthorName AS Author, c.CopyID, " +
            "       l.Issue_Date, l.Due_Date, l.Return_Date " +
            "FROM Loan l " +
            "JOIN BookCopy   c ON l.CopyID    = c.CopyID " +
            "JOIN Book       b ON c.BookID    = b.BookID " +
            "JOIN BookAuthor a ON b.AuthorID  = a.AuthorID " +
            "JOIN Member     m ON l.MemberID  = m.MemberID " +
            "ORDER BY l.LoanID";
        try (Statement st = con.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            printResultSet(rs);
        } catch (SQLException e) {
            System.err.println("Join query failed: " + e.getMessage());
        }
    }

    // ---------- helpers ----------
    private static void printResultSet(ResultSet rs) throws SQLException {
        ResultSetMetaData md = rs.getMetaData();
        int cols = md.getColumnCount();
        StringBuilder header = new StringBuilder();
        for (int i = 1; i <= cols; i++) header.append(md.getColumnLabel(i)).append("\t");
        System.out.println(header);
        while (rs.next()) {
            StringBuilder row = new StringBuilder();
            for (int i = 1; i <= cols; i++) row.append(rs.getString(i)).append("\t");
            System.out.println(row);
        }
    }

    private static int readInt(Scanner sc) {
        while (!sc.hasNextInt()) { sc.next(); System.out.print("Enter a number: "); }
        int v = sc.nextInt();
        sc.nextLine();
        return v;
    }
}
