from src.main.repositories import tour_repository, booking_repository
from src.main.services import booking_service

def client_menu(user):
    """Меню для клиента."""
    while True:
        print(f"\n===== Меню клиента ({user.name}, Баланс: {user.balance} руб.) =====")
        print("1. Посмотреть доступные путёвки")
        print("2. Мои бронирования")
        print("0. Выйти")
        
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            tours = tour_repository.get_all()
            print("\n--- Доступные путёвки ---")
            for t in tours:
                print(f"[{t.tour_id}] {t.destination} | Цена: {t.price} | Свободно мест: {t.seats_available}")
            
            try:
                tour_id_str = input("\nВведите ID путёвки для оформления (или Enter, чтобы отмена): ").strip()
                if tour_id_str:
                    tour_id = int(tour_id_str)
                    booking_service.create_booking(user.user_id, tour_id, manager_id=2)
                    print("\n[Успех] Путёвка оформлена!")
                    # Обновляем данные пользователя, чтобы увидеть новый баланс
                    from src.main.repositories import user_repository
                    user = user_repository.get_by_id(user.user_id) 
            except Exception as e:
                print(f"\n[Ошибка] {e}")

        elif choice == "2":
            bookings = booking_repository.get_all()
            my_bookings = [b for b in bookings if b.user_id == user.user_id]
            print("\n--- Мои бронирования ---")
            if not my_bookings:
                print("У вас пока нет бронирований.")
            for b in my_bookings:
                print(f"[{b.booking_id}] {b.tour_destination} | Статус: {b.status_name} | Сумма: {b.total_price}")

        elif choice == "0":
            break
        else:
            print("\n[Ошибка] Неверный пункт меню.")

def manager_menu(user):
    """Меню для менеджера."""
    while True:
        print(f"\n===== Меню менеджера ({user.name}) =====")
        print("1. Список всех путёвок")
        print("2. Все бронирования")
        print("3. Управление менеджерами")
        print("0. Выйти")
        
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            tours = tour_repository.get_all()
            print("\n--- Список путёвок ---")
            for t in tours:
                print(f"[{t.tour_id}] {t.destination} | Цена: {t.price} | Мест: {t.seats_available}/{t.seats_total}")
                
        elif choice == "2":
            bookings = booking_repository.get_all()
            print("\n--- Все бронирования ---")
            for b in bookings:
                print(f"[{b.booking_id}] Клиент: {b.client_name} | Путёвка: {b.tour_destination} | Статус: {b.status_name} | {b.total_price} руб.")
                
        elif choice == "3":
            managers_menu(user) # Переходим в подменю
            
        elif choice == "0":
            break
        else:
            print("\n[Ошибка] Неверный пункт меню.")


def managers_menu(current_user):
    """Подменю управления менеджерами."""
    from src.main.repositories import user_repository
    from src.main.services import auth_service

    while True:
        print("\n--- Управление менеджерами ---")
        print("1. Список менеджеров")
        print("2. Добавить менеджера")
        print("3. Удалить менеджера")
        print("0. Назад")
        
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            managers = user_repository.get_all_managers()
            print("\nСписок менеджеров:")
            for m in managers:
                print(f"[{m.user_id}] {m.surname} {m.name} | {m.email}")

        elif choice == "2":
            print("\n--- Добавление менеджера ---")
            name = input("Имя: ").strip()
            surname = input("Фамилия: ").strip()
            patronymic = input("Отчество (можно пропустить): ").strip() or None
            phone = input("Телефон: ").strip()
            email = input("Email: ").strip()
            password = input("Пароль: ").strip()
            try:
                auth_service.register_manager(name, surname, patronymic, phone, email, password)
                print("\n[Успех] Новый менеджер успешно добавлен!")
            except Exception as e:
                print(f"\n[Ошибка] {e}")

        elif choice == "3":
            managers = user_repository.get_all_managers()
            print("\nСписок менеджеров:")
            for m in managers:
                print(f"[{m.user_id}] {m.surname} {m.name} | {m.email}")
                
            id_str = input("\nВведите ID менеджера для удаления (или Enter, чтобы отмена): ").strip()
            if id_str:
                try:
                    m_id = int(id_str)
                    if m_id == current_user.user_id:
                        print("\n[Ошибка] Вы не можете удалить самого себя!")
                    else:
                        user_repository.delete(m_id)
                        print("\n[Успех] Менеджер удален.")
                except ValueError:
                    print("\n[Ошибка] ID должен быть числом.")
                except Exception as e:
                    print(f"\n[Ошибка] {e}")

        elif choice == "0":
            break
        else:
            print("\n[Ошибка] Неверный пункт меню.")