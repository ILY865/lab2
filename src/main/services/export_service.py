import json
import csv
import xml.etree.ElementTree as ET
import yaml
from pathlib import Path
from src.main.repositories import tour_repository, booking_repository

# Путь к папке out (находится в корне проекта)
OUT_DIR = Path(__file__).resolve().parents[3] / "out"

def _ensure_out_dir():
    """Создает папку out, если её нет."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)

def export_tours():
    """Выгружает путёвки во все форматы."""
    _ensure_out_dir()
    tours = tour_repository.get_all()
    
    # Преобразуем объекты в словари
    data = []
    for t in tours:
        data.append({
            "id": t.tour_id,
            "destination": t.destination,
            "dates": {"start": t.start_date, "end": t.end_date}, # Вложенность
            "price": t.price,
            "seats": {"total": t.seats_total, "available": t.seats_available}
        })
    
    _save_all_formats(data, "tours")

def export_bookings():
    """Выгружает бронирования (со связями) во все форматы."""
    _ensure_out_dir()
    bookings = booking_repository.get_all()
    
    data = []
    for b in bookings:
        data.append({
            "booking_id": b.booking_id,
            "client": b.client_name, # Связанные данные
            "tour": b.tour_destination, # Связанные данные
            "status": b.status_name, # Связанные данные
            "total_price": b.total_price
        })
        
    _save_all_formats(data, "bookings")

def _save_all_formats(data, base_filename):
    """Сохраняет данные в 4 формата."""
    if not data:
        print("Нет данных для экспорта.")
        return

    # 1. JSON
    json_path = OUT_DIR / f"{base_filename}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 2. CSV (для Excel: используем точку с запятой и кодировку windows-1251)
    csv_path = OUT_DIR / f"{base_filename}.csv"
    with open(csv_path, "w", encoding="windows-1251", newline="", errors="replace") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys(), delimiter=';')
        writer.writeheader()
        # Для вложенных словарей делаем строку (например, dates -> "start: ... | end: ...")
        for row in data:
            flat_row = {}
            for k, v in row.items():
                if isinstance(v, dict):
                    flat_row[k] = str(v)
                else:
                    flat_row[k] = v
            writer.writerow(flat_row)

    # 3. XML
    xml_path = OUT_DIR / f"{base_filename}.xml"
    root = ET.Element("root")
    for item in data:
        record = ET.SubElement(root, "record")
        for key, value in item.items():
            if isinstance(value, dict):
                sub_elem = ET.SubElement(record, key)
                for sub_k, sub_v in value.items():
                    child = ET.SubElement(sub_elem, sub_k)
                    child.text = str(sub_v)
            else:
                child = ET.SubElement(record, key)
                child.text = str(value)
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)

    # 4. YAML
    yaml_path = OUT_DIR / f"{base_filename}.yaml"
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

    print(f"\n[Успех] Данные выгружены в папку out/:")
    print(f" - {base_filename}.json")
    print(f" - {base_filename}.csv")
    print(f" - {base_filename}.xml")
    print(f" - {base_filename}.yaml")