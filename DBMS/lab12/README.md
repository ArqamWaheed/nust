# Lab 12 – Advanced JDBC: Issue Tracker

A Java/JDBC menu-driven application for an Issue Tracker built on a
normalized (3NF) schema.

## Schema (3NF)
- **User**(user_id PK, name, email UNIQUE)
- **Staff**(staff_id PK, name, role)
- **Issue**(issue_id PK, title, description, status DEFAULT 'Pending')
- **Assignment**(assign_id PK, issue_id UNIQUE → Issue, staff_id → Staff)

The `UNIQUE` on `Assignment.issue_id` enforces *one issue can only be
assigned once* at the database level.

## Setup
1. Load the schema:
   ```
   mysql -u root -p < schema.sql
   ```
2. Compile & run:
   ```
   javac IssueTrackerApp.java
   java -cp .:mysql-connector-j-8.4.0.jar IssueTrackerApp
   ```
   (On Windows use `;` instead of `:` in `-cp`.)

Update `URL`, `USER`, `PASS` in `IssueTrackerApp.java` if your credentials
differ (defaults: `root` / `root` / `IssueTrackerDB`).

## Features
- JDBC connection with success / failure message
- Menu-driven CRUD: register user, create / assign / view / update /
  delete / search issue
- LEFT JOIN across Issue ↔ Assignment ↔ Staff
- Controlled delete (refuses to delete assigned issues)
- Duplicate-assignment caught via UNIQUE constraint
- try-with-resources + try/catch on every JDBC call
- All `Connection`, `PreparedStatement`, `ResultSet`, `Scanner` auto-closed
