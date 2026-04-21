DROP DATABASE IF EXISTS LibraryDB;
CREATE DATABASE LibraryDB;
USE LibraryDB;

CREATE TABLE Librarian (
    LibrarianID   INT PRIMARY KEY,
    LibrarianName VARCHAR(100) NOT NULL,
    Email         VARCHAR(100),
    Phone         VARCHAR(20)
);

CREATE TABLE Member (
    MemberID       INT PRIMARY KEY,
    MemberName     VARCHAR(100) NOT NULL,
    MembershipDate DATE,
    Status         VARCHAR(20)
);

CREATE TABLE BookAuthor (
    AuthorID   INT PRIMARY KEY,
    AuthorName VARCHAR(100) NOT NULL
);

CREATE TABLE Book (
    BookID   INT PRIMARY KEY,
    BookName VARCHAR(150) NOT NULL,
    AuthorID INT,
    Category VARCHAR(50),
    FOREIGN KEY (AuthorID) REFERENCES BookAuthor(AuthorID)
);

CREATE TABLE BookCopy (
    CopyID INT PRIMARY KEY,
    BookID INT,
    Status VARCHAR(20),
    FOREIGN KEY (BookID) REFERENCES Book(BookID)
);

CREATE TABLE Loan (
    LoanID      INT PRIMARY KEY,
    CopyID      INT,
    MemberID    INT,
    Issue_Date  DATE,
    Due_Date    DATE,
    Return_Date DATE,
    FOREIGN KEY (CopyID)   REFERENCES BookCopy(CopyID),
    FOREIGN KEY (MemberID) REFERENCES Member(MemberID)
);

CREATE TABLE Fee (
    PaymentID INT PRIMARY KEY,
    MemberID  INT,
    FOREIGN KEY (MemberID) REFERENCES Member(MemberID)
);

-- Sample data
INSERT INTO Librarian VALUES
    (1, 'Ahmed Raza', 'ahmed@lib.com',  '0300-1111111'),
    (2, 'Sana Iqbal', 'sana@lib.com',   '0300-2222222');

INSERT INTO Member VALUES
    (1, 'Ali Khan',   '2025-01-10', 'ACTIVE'),
    (2, 'Sara Ahmed', '2025-02-15', 'ACTIVE'),
    (3, 'Bilal Tariq','2024-12-05', 'INACTIVE');

INSERT INTO BookAuthor VALUES
    (1, 'George Orwell'),
    (2, 'Chinua Achebe'),
    (3, 'Harper Lee');

INSERT INTO Book VALUES
    (1, '1984',                  1, 'Fiction'),
    (2, 'Animal Farm',           1, 'Fiction'),
    (3, 'Things Fall Apart',     2, 'Fiction'),
    (4, 'To Kill a Mockingbird', 3, 'Classic');

INSERT INTO BookCopy VALUES
    (101, 1, 'AVAILABLE'),
    (102, 1, 'ISSUED'),
    (103, 3, 'AVAILABLE'),
    (104, 4, 'AVAILABLE');

INSERT INTO Loan VALUES
    (1001, 102, 1, '2026-04-01', '2026-04-15', NULL),
    (1002, 103, 2, '2026-04-05', '2026-04-19', '2026-04-15');

INSERT INTO Fee VALUES
    (5001, 1),
    (5002, 2);
