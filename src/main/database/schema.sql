DROP TABLE IF EXISTS Booking;
DROP TABLE IF EXISTS Status;
DROP TABLE IF EXISTS Tour;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS UserRole;

CREATE TABLE UserRole (
    roleID   INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT NOT NULL UNIQUE
);

CREATE TABLE User (
    userID        INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    surname       TEXT NOT NULL,
    patronymic    TEXT,
    phone         TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    password      TEXT NOT NULL,
    balance       REAL NOT NULL DEFAULT 0.0,
    roleID        INTEGER NOT NULL,
    FOREIGN KEY (roleID) REFERENCES UserRole (roleID)
);

CREATE TABLE Tour (
    tourID           INTEGER PRIMARY KEY AUTOINCREMENT,
    destination      TEXT NOT NULL,
    start_date       TEXT NOT NULL,
    end_date         TEXT NOT NULL,
    price            REAL NOT NULL,
    seats_total      INTEGER NOT NULL,
    seats_available  INTEGER NOT NULL
);

CREATE TABLE Status (
    statusID  INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT NOT NULL UNIQUE
);

CREATE TABLE Booking (
    bookingID     INTEGER PRIMARY KEY AUTOINCREMENT,
    userID        INTEGER NOT NULL,
    tourID        INTEGER NOT NULL,
    managerID     INTEGER NOT NULL,
    statusID      INTEGER NOT NULL,
    total_price   REAL NOT NULL,
    FOREIGN KEY (userID)    REFERENCES User (userID),
    FOREIGN KEY (tourID)    REFERENCES Tour (tourID),
    FOREIGN KEY (managerID) REFERENCES User (userID),
    FOREIGN KEY (statusID)  REFERENCES Status (statusID)
);

INSERT INTO UserRole (name) VALUES
    ('Клиент'),
    ('Менеджер');

INSERT INTO User (name, surname, patronymic, phone, email, password, balance, roleID) VALUES
    ('Иван',  'Петров',  'Иванович', '+7-900-111-11-11', 'ivan@mail.ru',  'hash1', 5000.0, 1),
    ('Пётр',  'Смирнов', NULL,       '+7-900-222-22-22', 'petr@mail.ru',  'hash2', 0.0,    2);

INSERT INTO Tour (destination, start_date, end_date, price, seats_total, seats_available) VALUES
    ('Сочи',   '2026-06-01', '2026-06-10', 45000.00, 20, 15),
    ('Турция', '2026-07-05', '2026-07-15', 89000.00, 30, 30);

INSERT INTO Status (name) VALUES
    ('Оформлена'),
    ('Отменена');

INSERT INTO Booking (userID, tourID, managerID, statusID, total_price) VALUES
    (1, 1, 2, 1, 45000.0),
    (1, 2, 2, 2, 89000.0);