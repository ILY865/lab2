from src.main.services import auth_service

def login_screen():
    """Экран входа в систему."""
    print("\n--- Вход в систему ---")
    email = input("Email: ").strip()
    password = input("Пароль: ").strip()

    user = auth_service.authenticate(email, password)
    if user:
        print(f"\nДобро пожаловать, {user.name}!")
        return user
    else:
        print("\n[Ошибка] Неверный email или пароль.")
        return None

def register_screen():
    """Экран регистрации клиента (публичная)."""
    print("\n--- Регистрация клиента ---")
    name = input("Имя: ").strip()
    surname = input("Фамилия: ").strip()
    patronymic = input("Отчество (можно пропустить): ").strip() or None
    phone = input("Телефон: ").strip()
    email = input("Email: ").strip()
    password = input("Пароль: ").strip()

    try:
        # Вызываем сервис регистрации клиента (role_id=1)
        auth_service.register_client(name, surname, patronymic, phone, email, password)
        print("\n[Успех] Регистрация прошла успешно! Теперь вы можете войти.")
    except Exception as e:
        print(f"\n[Ошибка] {e}")