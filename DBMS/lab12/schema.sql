-- Lab 12 – Advanced JDBC: Issue Tracker
-- Normalized schema (3NF) with referential integrity

DROP DATABASE IF EXISTS IssueTrackerDB;
CREATE DATABASE IssueTrackerDB;
USE IssueTrackerDB;

CREATE TABLE User (
    user_id   INT AUTO_INCREMENT PRIMARY KEY,
    name      VARCHAR(60) NOT NULL,
    email     VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE Staff (
    staff_id  INT AUTO_INCREMENT PRIMARY KEY,
    name      VARCHAR(60) NOT NULL,
    role      VARCHAR(40) NOT NULL
);

CREATE TABLE Issue (
    issue_id     INT AUTO_INCREMENT PRIMARY KEY,
    title        VARCHAR(120) NOT NULL,
    description  TEXT,
    status       VARCHAR(20) NOT NULL DEFAULT 'Pending'
);

CREATE TABLE Assignment (
    assign_id  INT AUTO_INCREMENT PRIMARY KEY,
    issue_id   INT NOT NULL UNIQUE,
    staff_id   INT NOT NULL,
    CONSTRAINT fk_assign_issue FOREIGN KEY (issue_id) REFERENCES Issue(issue_id),
    CONSTRAINT fk_assign_staff FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

-- Sample staff
INSERT INTO Staff (name, role) VALUES
 ('Hassan Raza',  'Support Engineer'),
 ('Ayesha Noor',  'Senior Engineer'),
 ('Bilal Tariq',  'Network Admin');

-- Sample users
INSERT INTO User (name, email) VALUES
 ('Ali Khan',    'ali@nust.edu.pk'),
 ('Sara Ahmed',  'sara@nust.edu.pk');

-- Sample issues
INSERT INTO Issue (title, description, status) VALUES
 ('Wifi not working',     'Cannot connect to campus wifi from CR-1.', 'Pending'),
 ('Projector flickering', 'Projector in lab flickers every 10s.',     'Pending');
