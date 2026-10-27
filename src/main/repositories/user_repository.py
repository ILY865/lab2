from src.main.database.database import get_connection
from src.main.models.user import User

def _map(row) -> User:
    return User(
        user_id=row["userID"],
        name=row["name"],
        surname=row["surname"],
        patronymic=row["patronymic"],
        phone=row["phone"],
        email=row["email"],
        password=row["password"],
        balance=row["balance"],
        role_id=row["roleID"],
        role_name=row["role_name"] if "role_name" in row.keys() else None
    )

def get_by_email(email: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.*, r.name AS role_name 
        FROM User u 
        JOIN UserRole r ON u.roleID = r.roleID 
        WHERE u.email = ?
    """, (email,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_by_id(user_id: int) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.*, r.name AS role_name 
        FROM User u 
        JOIN UserRole r ON u.roleID = r.roleID 
        WHERE u.userID = ?
    """, (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def update_balance(user_id: int, new_balance: float):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE User SET balance = ? WHERE userID = ?", (new_balance, user_id))
    conn.commit()
    conn.close()

def create(name: str, surname: str, patronymic: str | None, phone: str, email: str, password: str, role_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO User (name, surname, patronymic, phone, email, password, balance, roleID)
        VALUES (?, ?, ?, ?, ?, ?, 0.0, ?)
    """, (name, surname, patronymic, phone, email, password, role_id))
    conn.commit()
    conn.close()

def get_all_managers() -> list[User]:
    """Возвращает список всех пользователей с ролью Менеджер (roleID = 2)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.*, r.name AS role_name 
        FROM User u 
        JOIN UserRole r ON u.roleID = r.roleID 
        WHERE u.roleID = 2
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def delete(user_id: int):
    """Удаляет пользователя по ID."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM User WHERE userID = ?", (user_id,))
    conn.commit()
    conn.close()

def get_all_clients() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.*, r.name AS role_name 
        FROM User u JOIN UserRole r ON u.roleID = r.roleID 
        WHERE u.roleID = 1
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]