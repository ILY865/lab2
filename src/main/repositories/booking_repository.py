from src.main.database.database import get_connection
from src.main.models.booking import Booking

def _map(row) -> Booking:
    return Booking(
        booking_id=row["bookingID"],
        user_id=row["userID"],
        tour_id=row["tourID"],
        manager_id=row["managerID"],
        status_id=row["statusID"],
        total_price=row["total_price"],
        client_name=row["client_name"] if "client_name" in row.keys() else None,
        tour_destination=row["tour_destination"] if "tour_destination" in row.keys() else None,
        status_name=row["status_name"] if "status_name" in row.keys() else None
    )

def get_all() -> list[Booking]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.*, 
               u.surname || ' ' || u.name AS client_name, 
               t.destination AS tour_destination, 
               s.name AS status_name
        FROM Booking b
        JOIN User u ON b.userID = u.userID
        JOIN Tour t ON b.tourID = t.tourID
        JOIN Status s ON b.statusID = s.statusID
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def create(user_id: int, tour_id: int, manager_id: int, total_price: float):
    conn = get_connection()
    cur = conn.cursor()
    # statusID = 1 (Оформлена)
    cur.execute("""
        INSERT INTO Booking (userID, tourID, managerID, statusID, total_price)
        VALUES (?, ?, ?, 1, ?)
    """, (user_id, tour_id, manager_id, total_price))
    conn.commit()
    conn.close()


def get_by_id(booking_id: int) -> Booking | None:
    """Получает бронь по её ID."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Booking WHERE bookingID = ?", (booking_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def cancel_booking(booking_id: int):
    """Меняет статус брони на 2 (Отменена)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Booking SET statusID = 2 WHERE bookingID = ?", (booking_id,))
    conn.commit()
    conn.close()