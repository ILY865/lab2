from src.main.repositories import tour_repository, booking_repository, user_repository


def create_booking(user_id: int, tour_id: int, manager_id: int):
    """Оформляет путёвку с проверкой баланса и наличия мест."""
    # 1. Получаем данные клиента и путёвки
    user = user_repository.get_by_id(user_id)
    if not user:
        raise Exception("Клиент не найден")

    tour = tour_repository.get_by_id(tour_id)
    if not tour:
        raise Exception("Путёвка не найдена")
        
    if tour.seats_available <= 0:
        raise Exception("На эту путёвку нет свободных мест")
        
    # 2. Проверяем баланс
    if user.balance < tour.price:
        raise Exception(f"Недостаточно средств. Баланс: {user.balance} руб., нужно: {tour.price} руб.")
        
    # 3. Списываем деньги и уменьшаем количество мест
    new_balance = user.balance - tour.price
    user_repository.update_balance(user.user_id, new_balance)
    
    tour_repository.update(tour.tour_id, tour.destination, tour.price, tour.seats_available - 1)
    
    # 4. Создаем бронь
    booking_repository.create(user_id, tour_id, manager_id, tour.price)
    
    return True


def cancel_booking(booking_id: int):
    """Отменяет бронь и возвращает место в путёвку."""
    # 1. Находим бронь
    booking = booking_repository.get_by_id(booking_id)
    if not booking:
        raise Exception("Бронь с таким ID не найдена")
        
    if booking.status_id == 2:
        raise Exception("Эта бронь уже отменена")

    # 2. Находим путёвку, на которую была бронь
    tour = tour_repository.get_by_id(booking.tour_id)
    
    # 3. Отменяем бронь (меняем статус в БД)
    booking_repository.cancel_booking(booking_id)
    
    # 4. Возвращаем место обратно в путёвку (+1 к свободным местам)
    if tour:
        tour_repository.update(
            tour_id=tour.tour_id, 
            destination=tour.destination, 
            price=tour.price, 
            seats_available=tour.seats_available + 1
        )
        
    return True