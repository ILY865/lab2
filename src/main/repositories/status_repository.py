from src.main.database.database import get_connection
from src.main.models.status import Status

def _map(row) -> Status:
    return Status(status_id=row["statusID"], name=row["name"])

def get_all() -> list[Status]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Status")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]