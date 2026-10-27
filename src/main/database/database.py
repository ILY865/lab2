import sqlite3
from pathlib import Path


# Путь к файлу базы данных (создаётся в корне проекта)
DB_PATH = Path(__file__).resolve().parents[3] / "tour_agency.db"

# Путь к SQL-скрипту со схемой
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def get_connection():
    """Возвращает соединение с базой данных SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Создаёт базу данных из schema.sql (если ещё не создана)."""
    if DB_PATH.exists():
        return  # База уже существует, молча выходим

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn = get_connection()
    try:
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()


def get_all_tours():
    """Возвращает список всех путёвок."""
    conn = get_connection()
    try:
        cur = conn.execute("SELECT * FROM Tour")
        return cur.fetchall()
    finally:
        conn.close()


def get_all_users():
    """Возвращает список всех пользователей с их ролями."""
    conn = get_connection()
    try:
        cur = conn.execute("""
            SELECT u.userID, u.name, u.surname, u.email, r.name AS role
            FROM User u
            JOIN UserRole r ON u.roleID = r.roleID
        """)
        return cur.fetchall()
    finally:
        conn.close()


def get_all_bookings():
    """Возвращает список всех бронирований с деталями."""
    conn = get_connection()
    try:
        cur = conn.execute("""
            SELECT
                b.bookingID,
                u.surname || ' ' || u.name AS client,
                t.destination AS tour,
                s.name AS status,
                b.total_price
            FROM Booking b
            JOIN User u ON b.userID = u.userID
            JOIN Tour t ON b.tourID = t.tourID
            JOIN Status s ON b.statusID = s.statusID
        """)
        return cur.fetchall()
    finally:
        conn.close()