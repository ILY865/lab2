from src.main.repositories import user_repository
from src.main.models.user import User


def authenticate(email: str, password: str) -> User | None:
    """Проверяет логин и пароль. Возвращает пользователя или None."""
    user = user_repository.get_by_email(email)
    
    if not user:
        return None
        
    if user.password != password:
        return None
        
    return user


def register_client(name: str, surname: str, patronymic: str | None, phone: str, email: str, password: str):
    """Регистрирует нового клиента (role_id=1)."""
    if not name.strip() or not surname.strip():
        raise Exception("Имя и фамилия не могут быть пустыми")
    if not email or "@" not in email:
        raise Exception("Некорректный email")
    if len(password) < 5:
        raise Exception("Пароль должен быть не менее 5 символов")

    existing = user_repository.get_by_email(email)
    if existing:
        raise Exception("Пользователь с таким email уже существует")

    user_repository.create(name, surname, patronymic, phone, email, password, role_id=1)

def register_manager(name: str, surname: str, patronymic: str | None, phone: str, email: str, password: str):
    """Регистрирует нового менеджера (role_id=2). Вызывается только из меню менеджера."""
    if not name.strip() or not surname.strip():
        raise Exception("Имя и фамилия не могут быть пустыми")
    if not email or "@" not in email:
        raise Exception("Некорректный email")
    if len(password) < 5:
        raise Exception("Пароль должен быть не менее 5 символов")

    existing = user_repository.get_by_email(email)
    if existing:
        raise Exception("Пользователь с таким email уже существует")

    user_repository.create(name, surname, patronymic, phone, email, password, role_id=2)