import java.io.FileInputStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import java.util.Scanner;

public class FinanceApp {

    static String URL;
    static String USER;
    static String PASS;
    static String DB_NAME = "finance_tracker";

    public static void main(String[] args) {
        try {
            loadConfig();
        } catch (Exception e) {
            System.out.println("Could not read db.properties: " + e.getMessage());
            return;
        }

        try {
            bootstrapIfNeeded();
        } catch (Exception e) {
            System.out.println("Bootstrap failed: " + e.getMessage());
            return;
        }

        try (Connection con = DriverManager.getConnection(URL, USER, PASS);
             Scanner sc = new Scanner(System.in)) {

            System.out.println("Connected to MySQL (" + DB_NAME + ") successfully.");

            while (true) {
                System.out.println();
                System.out.println("===== Finance Tracker =====");
                System.out.println("1. List Users");
                System.out.println("2. List Accounts (with balance)");
                System.out.println("3. Add Transaction (income / expense)");
                System.out.println("4. Transfer Between Accounts");
                System.out.println("5. View Net Worth");
                System.out.println("6. View Budget Status");
                System.out.println("7. View Portfolio");
                System.out.println("8. Exit");
                System.out.print("Choice: ");
                String choice = sc.nextLine().trim();

                switch (choice) {
                    case "1": listUsers(con);            break;
                    case "2": listAccounts(con);         break;
                    case "3": addTransaction(con, sc);   break;
                    case "4": transfer(con, sc);         break;
                    case "5": viewNetWorth(con);         break;
                    case "6": viewBudgetStatus(con, sc); break;
                    case "7": viewPortfolio(con);        break;
                    case "8": System.out.println("Goodbye."); return;
                    default : System.out.println("Invalid choice.");
                }
            }
        } catch (SQLException e) {
            System.out.println("Connection failed: " + e.getMessage());
        }
    }

    // ---------- config ----------
    static void loadConfig() throws Exception {
        Properties p = new Properties();
        try (FileInputStream in = new FileInputStream("db.properties")) {
            p.load(in);
        }
        URL  = p.getProperty("url",  "jdbc:mysql://localhost:3306/finance_tracker");
        USER = p.getProperty("user", "root");
        PASS = p.getProperty("password", "");
    }

    // ---------- bootstrap: create DB / load schema / load sample data on first run ----------
    static void bootstrapIfNeeded() throws Exception {
        // strip "/<dbname>" so we can connect without requiring the DB to exist yet
        String serverUrl = URL.replaceAll("/" + DB_NAME + "(\\?.*)?$", "/$1");
        if (serverUrl.endsWith("/")) serverUrl = serverUrl.substring(0, serverUrl.length() - 1);

        try (Connection con = DriverManager.getConnection(serverUrl, USER, PASS);
             Statement st = con.createStatement()) {

            boolean dbExists;
            try (ResultSet rs = st.executeQuery(
                    "SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = '" + DB_NAME + "'")) {
                dbExists = rs.next();
            }

            if (!dbExists) {
                System.out.println("Database '" + DB_NAME + "' not found. Loading schema.sql ...");
                runSqlFile(con, "schema.sql");
                System.out.println("Schema loaded. Loading sample_data.sql ...");
                runSqlFile(con, "sample_data.sql");
                System.out.println("Sample data loaded.");
                return;
            }

            // DB exists — make sure tables exist, otherwise load schema
            st.execute("USE " + DB_NAME);
            boolean hasUsers;
            try (ResultSet rs = st.executeQuery(
                    "SELECT TABLE_NAME FROM information_schema.TABLES " +
                    "WHERE TABLE_SCHEMA = '" + DB_NAME + "' AND TABLE_NAME = 'users'")) {
                hasUsers = rs.next();
            }
            if (!hasUsers) {
                System.out.println("Tables missing. Loading schema.sql ...");
                runSqlFile(con, "schema.sql");
            }

            // load sample data only if users table is empty
            try (ResultSet rs = st.executeQuery("SELECT COUNT(*) FROM " + DB_NAME + ".users")) {
                rs.next();
                if (rs.getInt(1) == 0) {
                    System.out.println("No users found. Loading sample_data.sql ...");
                    runSqlFile(con, "sample_data.sql");
                }
            }
        }
    }

    // run a .sql file, honouring `DELIMITER ...` directives so triggers/procedures load correctly
    static void runSqlFile(Connection con, String path) throws Exception {
        String content = new String(Files.readAllBytes(Paths.get(path)));
        List<String> stmts = splitSql(content);
        try (Statement st = con.createStatement()) {
            for (String s : stmts) {
                String trimmed = s.trim();
                if (trimmed.isEmpty()) continue;
                st.execute(trimmed);
            }
        }
    }

    // tiny splitter: handles `DELIMITER xxx` lines and ignores -- line comments
    static List<String> splitSql(String sql) {
        List<String> out = new ArrayList<>();
        String delim = ";";
        StringBuilder cur = new StringBuilder();
        for (String rawLine : sql.split("\\r?\\n")) {
            String line = rawLine;
            String stripped = line.trim();
            if (stripped.startsWith("--") || stripped.isEmpty()) continue;
            if (stripped.toUpperCase().startsWith("DELIMITER ")) {
                if (cur.toString().trim().length() > 0) {
                    out.add(cur.toString());
                    cur.setLength(0);
                }
                delim = stripped.substring("DELIMITER ".length()).trim();
                continue;
            }
            cur.append(line).append('\n');
            // flush whenever the buffer ends with the active delimiter
            String buf = cur.toString().trim();
            if (buf.endsWith(delim)) {
                String stmt = buf.substring(0, buf.length() - delim.length());
                out.add(stmt);
                cur.setLength(0);
            }
        }
        if (cur.toString().trim().length() > 0) out.add(cur.toString());
        return out;
    }

    // ---------- 1. List Users ----------
    static void listUsers(Connection con) {
        runReadQuery(con,
            "SELECT user_id, full_name, email, role, is_active FROM users ORDER BY user_id");
    }

    // ---------- 2. List Accounts ----------
    static void listAccounts(Connection con) {
        String sql =
            "SELECT a.account_id, u.full_name AS owner, a.account_name, " +
            "       t.type_name, a.currency_code, a.balance " +
            "FROM accounts a " +
            "JOIN users u         ON u.user_id = a.user_id " +
            "JOIN account_types t ON t.type_id = a.type_id " +
            "ORDER BY a.user_id, a.account_id";
        runReadQuery(con, sql);
    }

    // ---------- 3. Add Transaction ----------
    static void addTransaction(Connection con, Scanner sc) {
        System.out.print("Account ID: ");
        int accId = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Type (income / expense): ");
        String type = sc.nextLine().trim().toLowerCase();
        if (!type.equals("income") && !type.equals("expense")) {
            System.out.println("Invalid type.");
            return;
        }
        System.out.print("Category ID: ");
        int catId = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Amount: ");
        String amount = sc.nextLine().trim();
        System.out.print("Date (YYYY-MM-DD): ");
        String date = sc.nextLine().trim();
        System.out.print("Description: ");
        String desc = sc.nextLine().trim();

        String sql =
            "INSERT INTO transactions(account_id, category_id, txn_type, amount, txn_date, description) " +
            "VALUES (?,?,?,?,?,?)";
        try (PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, accId);
            ps.setInt(2, catId);
            ps.setString(3, type);
            ps.setBigDecimal(4, new java.math.BigDecimal(amount));
            ps.setDate(5, Date.valueOf(date));
            ps.setString(6, desc);
            int n = ps.executeUpdate();
            // trigger trg_txn_after_insert updates accounts.balance automatically
            System.out.println(n + " transaction(s) recorded. Balance auto-updated.");
        } catch (SQLException e) {
            System.out.println("Insert failed: " + e.getMessage());
        }
    }

    // ---------- 4. Transfer ----------
    static void transfer(Connection con, Scanner sc) {
        System.out.print("From account ID: ");
        int from = Integer.parseInt(sc.nextLine().trim());
        System.out.print("To account ID: ");
        int to = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Amount: ");
        String amount = sc.nextLine().trim();
        System.out.print("Date (YYYY-MM-DD): ");
        String date = sc.nextLine().trim();
        System.out.print("Note: ");
        String note = sc.nextLine().trim();

        // call the stored procedure so the transfer pair is atomic
        try (CallableStatement cs = con.prepareCall("{CALL sp_record_transfer(?,?,?,?,?)}")) {
            cs.setInt(1, from);
            cs.setInt(2, to);
            cs.setBigDecimal(3, new java.math.BigDecimal(amount));
            cs.setDate(4, Date.valueOf(date));
            cs.setString(5, note);
            cs.execute();
            System.out.println("Transfer recorded.");
        } catch (SQLException e) {
            System.out.println("Transfer failed: " + e.getMessage());
        }
    }

    // ---------- 5. Net Worth ----------
    static void viewNetWorth(Connection con) {
        runReadQuery(con,
            "SELECT user_id, full_name, cash_pkr, investments_pkr, net_worth_pkr " +
            "FROM v_net_worth ORDER BY user_id");
    }

    // ---------- 6. Budget Status ----------
    static void viewBudgetStatus(Connection con, Scanner sc) {
        System.out.print("User ID: ");
        int uid = Integer.parseInt(sc.nextLine().trim());
        String sql =
            "SELECT category_name, month_year, limit_amount, actual_spent, remaining, pct_used " +
            "FROM v_budget_status WHERE user_id = ? ORDER BY month_year DESC, category_name";
        try (PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, uid);
            printRs(ps);
        } catch (SQLException e) {
            System.out.println("Read failed: " + e.getMessage());
        }
    }

    // ---------- 7. Portfolio ----------
    static void viewPortfolio(Connection con) {
        runReadQuery(con,
            "SELECT user_id, asset_name, symbol, quantity, buy_price, current_price, " +
            "       cost_basis, market_value, gain_loss, roi_pct " +
            "FROM v_portfolio ORDER BY user_id, asset_name");
    }

    // ---------- helpers ----------
    static void printRs(PreparedStatement ps) throws SQLException {
        try (ResultSet rs = ps.executeQuery()) {
            ResultSetMetaData md = rs.getMetaData();
            int cols = md.getColumnCount();
            for (int i = 1; i <= cols; i++)
                System.out.print(md.getColumnLabel(i) + (i < cols ? "\t" : "\n"));
            int count = 0;
            while (rs.next()) {
                count++;
                for (int i = 1; i <= cols; i++)
                    System.out.print(rs.getString(i) + (i < cols ? "\t" : "\n"));
            }
            if (count == 0) System.out.println("(no rows)");
        }
    }

    static void runReadQuery(Connection con, String sql) {
        try (PreparedStatement ps = con.prepareStatement(sql)) {
            printRs(ps);
        } catch (SQLException e) {
            System.out.println("Read failed: " + e.getMessage());
        }
    }
}
