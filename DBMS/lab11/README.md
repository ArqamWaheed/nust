# Lab 11 – JDBC CRUD on LibraryDB (Normalized in Lab 10)

## Schema (already 3NF from Lab 10)
- **Librarian**(LibrarianID PK, LibrarianName, Email, Phone)
- **Member**(MemberID PK, MemberName, MembershipDate, Status)
- **BookAuthor**(AuthorID PK, AuthorName)
- **Book**(BookID PK, BookName, AuthorID → BookAuthor, Category)
- **BookCopy**(CopyID PK, BookID → Book, Status)
- **Loan**(LoanID PK, CopyID → BookCopy, MemberID → Member, Issue_Date, Due_Date, Return_Date)
- **Fee**(PaymentID PK, MemberID → Member)

## Setup
1. Load the schema:
   ```
   mysql -u root -p < schema.sql
   ```
2. Put MySQL Connector/J (e.g. `mysql-connector-j-8.x.x.jar`) in this folder.
3. Compile & run:
   ```
   javac LibraryApp.java
   java -cp .:mysql-connector-j-8.x.x.jar LibraryApp
   ```
   (On Windows use `;` instead of `:` in `-cp`.)

Update `URL`, `USER`, `PASS` in `LibraryApp.java` if your credentials differ
(defaults: `root` / `root` / `LibraryDB`).

## Features
- JDBC connection with success/failure message
- Menu-driven CRUD on all 7 tables using `PreparedStatement`
- JOIN across Loan ↔ BookCopy ↔ Book ↔ BookAuthor ↔ Member
- try-with-resources + try/catch throughout
- All `Connection`, `Statement`, `PreparedStatement`, `ResultSet`, `Scanner` auto-closed
