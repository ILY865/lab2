
import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[2] / "tour_agency.db"

SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"

def get_connection():
    """Возвращает соединение с базой данных SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Создаёт базу данных из schema.sql (если ещё не создана)."""
    if DB_PATH.exists():
        print(f"База данных уже существует: {DB_PATH.name}")
        return

    print(f"Создаю базу данных {DB_PATH.name}...")

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn = get_connection()
    try:
        conn.executescript(schema_sql)
        conn.commit()
        print("База данных успешно создана.")
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
                b.booking_date
            FROM Booking b
            JOIN User u ON b.userID = u.userID
            JOIN Tour t ON b.tourID = t.tourID
            JOIN Status s ON b.statusID = s.statusID
        """)
        return cur.fetchall()
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()

    print("\n=== Путёвки ===")
    for tour in get_all_tours():
        print(f"  [{tour['tourID']}] {tour['destination']} — "
              f"{tour['price']} руб., мест: {tour['seats_available']}/{tour['seats_total']}")

    print("\n=== Пользователи ===")
    for user in get_all_users():
        print(f"  [{user['userID']}] {user['surname']} {user['name']} "
              f"({user['role']}) — {user['email']}")

    print("\n=== Бронирования ===")
    for booking in get_all_bookings():
        print(f"  [{booking['bookingID']}] {booking['client']} → "
              f"{booking['tour']} ({booking['status']}), {booking['booking_date']}")