-- Роли
INSERT INTO UserRole (name) VALUES
    ('Клиент'),
    ('Менеджер');

-- Пользователи
INSERT INTO User (name, surname, patronimik, phone, email, password_hash, roleID) VALUES
    ('Иван',  'Петров',  'Иванович', '+7-900-111-11-11', 'ivan@mail.ru',  'hash1', 1),
    ('Пётр',  'Смирнов', NULL,       '+7-900-222-22-22', 'petr@mail.ru',  'hash2', 2);

-- Путёвки
INSERT INTO Tour (destination, start_date, end_date, price, seats_total, seats_available) VALUES
    ('Сочи',   '2026-06-01', '2026-06-10', 45000.00, 20, 15),
    ('Турция', '2026-07-05', '2026-07-15', 89000.00, 30, 30);

-- Статусы
INSERT INTO Status (name) VALUES
    ('Оформлена'),
    ('Отменена');

-- Бронирования
INSERT INTO Booking (userID, tourID, managerID, statusID, booking_date) VALUES
    (1, 1, 2, 1, '2026-05-01'),
    (1, 2, 2, 2, '2026-05-03');