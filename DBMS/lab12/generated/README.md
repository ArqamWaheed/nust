# Lab 12: Advanced JDBC - Issue Tracker

## Setup

1. Install MySQL and Java (JDK 17+).
2. Place `mysql-connector-j-9.x.x.jar` in this folder.
3. Load schema:
   ```
   mysql -u root -p < schema.sql
   ```
4. Compile and run:
   ```
   javac IssueApp.java
   java -cp ".;mysql-connector-j-9.6.0.jar" IssueApp
   ```
   On Linux replace `;` with `:` in `-cp`.

## Features

- Register users (email validated as non-empty)
- Create issues (default status Pending)
- Assign issues to staff (one-to-one constraint)
- View all issues with assigned staff (LEFT JOIN)
- Update status: Pending -> In Progress -> Resolved
- Controlled delete (assigned issues blocked)
- Search by status or issue id

All DB calls use PreparedStatement and try-with-resources.
