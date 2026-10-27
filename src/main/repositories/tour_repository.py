from src.main.database.database import get_connection
from src.main.models.tour import Tour


def _map(row) -> Tour:
    """Преобразует строку из БД в объект модели Tour."""
    return Tour(
        tour_id=row["tourID"],
        destination=row["destination"],
        start_date=row["start_date"],
        end_date=row["end_date"],
        price=row["price"],
        seats_total=row["seats_total"],
        seats_available=row["seats_available"]
    )


def create(destination: str, start_date: str, end_date: str, price: float, seats_total: int):
    """Create — добавление новой путёвки."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Tour (destination, start_date, end_date, price, seats_total, seats_available)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (destination, start_date, end_date, price, seats_total, seats_total))
    conn.commit()
    conn.close()


def get_by_id(tour_id: int) -> Tour | None:
    """Read — получение путёвки по ID."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tour WHERE tourID = ?", (tour_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[Tour]:
    """Read — получение списка всех путёвок."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tour")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def update(tour_id: int, destination: str, price: float, seats_available: int):
    """Update — обновление данных путёвки."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Tour 
        SET destination = ?, price = ?, seats_available = ?
        WHERE tourID = ?
    """, (destination, price, seats_available, tour_id))
    conn.commit()
    conn.close()


def delete(tour_id: int):
    """Delete — удаление путёвки."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Tour WHERE tourID = ?", (tour_id,))
    conn.commit()
    conn.close()