from src.main.repositories import tour_repository, booking_repository, user_repository
from src.main.services import booking_service, auth_service


def client_menu(user):
    """Меню для клиента."""
    while True:
        # Обновляем данные пользователя из БД, чтобы баланс всегда был актуальным
        user = user_repository.get_by_id(user.user_id)
        
        print(f"\n===== Меню клиента ({user.name}, Баланс: {user.balance} руб.) =====")
        print("1. Посмотреть доступные путёвки и оформить")
        print("2. Мои бронирования")
        print("3. Отменить бронирование")
        print("4. Пополнить баланс")
        print("0. Выйти")
        
        choice = input("Выберите действие: ").strip()

        # 1. Просмотр и оформление
        if choice == "1":
            tours = tour_repository.get_all()
            print("\n--- Доступные путёвки ---")
            for t in tours:
                # ДОБАВИЛИ ВЫВОД ДАТ
                print(f"[{t.tour_id}] {t.destination} | Даты: {t.start_date} - {t.end_date} | Цена: {t.price} | Свободно мест: {t.seats_available}")
            
            try:
                tour_id_str = input("\nВведите ID путёвки для оформления (или Enter, чтобы отмена): ").strip()
                if tour_id_str:
                    tour_id = int(tour_id_str)
                    booking_service.create_booking(user.user_id, tour_id, manager_id=2) # manager_id=2 - Арсений
                    print("\n[Успех] Путёвка оформлена!")
            except Exception as e:
                print(f"\n[Ошибка] {e}")

        # 2. Мои бронирования
        elif choice == "2":
            bookings = booking_repository.get_all()
            my_bookings = [b for b in bookings if b.user_id == user.user_id]
            print("\n--- Мои бронирования ---")
            if not my_bookings:
                print("У вас пока нет бронирований.")
            for b in my_bookings:
                print(f"[{b.booking_id}] {b.tour_destination} | Статус: {b.status_name} | Сумма: {b.total_price}")

        # 3. Отмена бронирования
        elif choice == "3":
            bookings = booking_repository.get_all()
            active_bookings = [b for b in bookings if b.user_id == user.user_id and b.status_id == 1]
            
            print("\n--- Ваши активные брони ---")
            if not active_bookings:
                print("У вас нет активных броней для отмены.")
            else:
                for b in active_bookings:
                    print(f"[{b.booking_id}] {b.tour_destination} | Сумма: {b.total_price}")
                
                try:
                    b_id_str = input("\nВведите ID брони для отмены (или Enter, чтобы отмена): ").strip()
                    if b_id_str:
                        b_id = int(b_id_str)
                        booking_service.cancel_booking(b_id)
                        print("\n[Успех] Бронь отменена, место возвращено в путёвку!")
                except Exception as e:
                    print(f"\n[Ошибка] {e}")

        # 4. Пополнение баланса
        elif choice == "4":
            try:
                amount_str = input("\nВведите сумму для пополнения (в рублях): ").strip()
                if amount_str:
                    amount = float(amount_str)
                    if amount <= 0:
                        print("\n[Ошибка] Сумма должна быть больше нуля.")
                    else:
                        new_balance = user.balance + amount
                        user_repository.update_balance(user.user_id, new_balance)
                        print(f"\n[Успех] Баланс пополнен на {amount} руб. Текущий баланс: {new_balance} руб.")
            except ValueError:
                print("\n[Ошибка] Введите корректное число.")
            except Exception as e:
                print(f"\n[Ошибка] {e}")

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
        print("3. Добавить новую путёвку")
        print("4. Изменить/Удалить путёвку")
        print("5. Управление менеджерами")
        print("6. Список клиентов")
        print("0. Выйти")
        
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            tours = tour_repository.get_all()
            print("\n--- Список путёвок ---")
            for t in tours:
                # ДОБАВИЛИ ВЫВОД ДАТ
                print(f"[{t.tour_id}] {t.destination} | {t.start_date} - {t.end_date} | Цена: {t.price} | Мест: {t.seats_available}/{t.seats_total}")
                
        elif choice == "2":
            bookings = booking_repository.get_all()
            print("\n--- Все бронирования ---")
            if not bookings:
                print("Бронирований пока нет.")
            for b in bookings:
                print(f"[{b.booking_id}] Клиент: {b.client_name} | Путёвка: {b.tour_destination} | Статус: {b.status_name} | {b.total_price} руб.")

        elif choice == "3":
            print("\n--- Добавление путёвки ---")
            try:
                dest = input("Направление: ").strip()
                start = input("Дата начала (ГГГГ-ММ-ДД): ").strip()
                end = input("Дата окончания (ГГГГ-ММ-ДД): ").strip()
                price = float(input("Цена: ").strip())
                seats = int(input("Количество мест: ").strip())
                tour_repository.create(dest, start, end, price, seats)
                print("\n[Успех] Путёвка добавлена!")
            except Exception as e:
                print(f"\n[Ошибка] {e}")

        elif choice == "4":
            tours = tour_repository.get_all()
            print("\n--- Список путёвок ---")
            for t in tours:
                # ДОБАВИЛИ ВЫВОД ДАТ
                print(f"[{t.tour_id}] {t.destination} | {t.start_date} - {t.end_date} | Цена: {t.price} | Мест: {t.seats_available}/{t.seats_total}")
            
            try:
                t_id_str = input("\nВведите ID путёвки для изменения (или Enter для отмены): ").strip()
                if t_id_str:
                    t_id = int(t_id_str)
                    tour = tour_repository.get_by_id(t_id)
                    if not tour:
                        print("\n[Ошибка] Путёвка не найдена.")
                    else:
                        print(f"Текущее направление: {tour.destination}")
                        new_dest = input("Новое направление (Enter - оставить): ").strip() or tour.destination
                        
                        # Для простоты не меняем даты, только цену и места
                        new_price_str = input(f"Новая цена (Enter - оставить {tour.price}): ").strip()
                        new_price = float(new_price_str) if new_price_str else tour.price
                        new_seats_str = input(f"Новые свободные места (Enter - оставить {tour.seats_available}): ").strip()
                        new_seats = int(new_seats_str) if new_seats_str else tour.seats_available
                        
                        tour_repository.update(t_id, new_dest, new_price, new_seats)
                        print("\n[Успех] Данные путёвки обновлены!")
                        
                        del_choice = input("Удалить эту путёвку полностью? (y/n): ").strip().lower()
                        if del_choice == 'y':
                            tour_repository.delete(t_id)
                            print("\n[Успех] Путёвка удалена.")
            except Exception as e:
                print(f"\n[Ошибка] {e}")

        elif choice == "5":
            managers_menu(user) # Переходим в подменю

        elif choice == "6":
            clients = user_repository.get_all_clients()
            print("\n--- Список клиентов ---")
            if not clients:
                print("Клиентов пока нет.")
            for c in clients:
                print(f"[{c.user_id}] {c.surname} {c.name} | {c.email} | Баланс: {c.balance} руб.")

        elif choice == "0":
            break
        else:
            print("\n[Ошибка] Неверный пункт меню.")


def managers_menu(current_user):
    """Подменю управления менеджерами."""
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