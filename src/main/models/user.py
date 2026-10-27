from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    name: str
    surname: str
    patronymic: str | None
    phone: str
    email: str
    password: str
    balance: float
    role_id: int
    # Служебное поле для удобного вывода (не из БД)
    role_name: str | None = None