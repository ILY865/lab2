from src.main.database.database import get_connection
from src.main.models.role import Role

def _map(row) -> Role:
    return Role(role_id=row["roleID"], name=row["name"])

def get_all() -> list[Role]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM UserRole")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(role_id: int) -> Role | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM UserRole WHERE roleID = ?", (role_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None