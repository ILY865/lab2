from dataclasses import dataclass

@dataclass
class Tour:
    tour_id: int
    destination: str
    start_date: str
    end_date: str
    price: float
    seats_total: int
    seats_available: int