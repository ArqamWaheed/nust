DROP DATABASE IF EXISTS issue_db;
CREATE DATABASE issue_db;
USE issue_db;

CREATE TABLE User (
    user_id INT PRIMARY KEY,
    name    VARCHAR(100) NOT NULL,
    email   VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE Issue (
    issue_id    INT AUTO_INCREMENT PRIMARY KEY,
    title       VARCHAR(200) NOT NULL,
    description TEXT,
    status      VARCHAR(20) NOT NULL DEFAULT 'Pending',
    user_id     INT NOT NULL,
    CONSTRAINT chk_status CHECK (status IN ('Pending','In Progress','Resolved')),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE Staff (
    staff_id INT PRIMARY KEY,
    name     VARCHAR(100) NOT NULL,
    role     VARCHAR(80)  NOT NULL
);

CREATE TABLE Assignment (
    assign_id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id  INT NOT NULL UNIQUE,
    staff_id  INT NOT NULL,
    FOREIGN KEY (issue_id) REFERENCES Issue(issue_id) ON DELETE CASCADE,
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

INSERT INTO Staff (staff_id, name, role) VALUES
    (10, 'Sir Fahad',    'IT Support'),
    (11, 'Saood Sarwar', 'Lab Engineer'),
    (12, 'Hina Khan',    'Network Admin');
