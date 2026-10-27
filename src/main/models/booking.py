from dataclasses import dataclass

@dataclass
class Booking:
    booking_id: int
    user_id: int
    tour_id: int
    manager_id: int
    status_id: int
    total_price: float
    # Служебные поля для удобного вывода (не из БД)
    client_name: str | None = None
    tour_destination: str | None = None
    status_name: str | None = None