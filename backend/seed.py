"""
Скрипт для додавання тестового шаблону до бази даних.
Запускати з папки backend: python seed.py
"""
import sys
import os

# Додаємо папку backend до шляху, щоб імпорти спрацювали
sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal, engine
import models

# Створюємо таблиці якщо їх немає
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Перевіряємо чи шаблон вже існує
existing = db.query(models.Template).filter(models.Template.id == 1).first()
if existing:
    print("Шаблон вже існує в базі даних!")
    db.close()
    sys.exit(0)

# Шлях до файлу шаблону (відносно папки backend)
template_path = os.path.join(os.path.dirname(__file__), "..", "templates", "dogovir_orendy.docx")
template_path = os.path.normpath(template_path)

if not os.path.exists(template_path):
    print(f"ПОМИЛКА: Файл шаблону не знайдено за шляхом: {template_path}")
    print("Спочатку створи файл dogovir_orendy.docx у папці templates/")
    db.close()
    sys.exit(1)

# Додаємо запис у базу даних
template = models.Template(
    name="Договір оренди житла",
    description="Стандартний договір оренди жилого приміщення між орендодавцем та орендарем",
    file_path=template_path,
    # fields_config — це конфігурація анкети (які поля показувати юзеру)
    fields_config={
        "contract_number": {"label": "Номер договору", "type": "text", "required": True},
        "city":            {"label": "Місто укладення", "type": "text", "required": True},
        "date":            {"label": "Дата договору (напр. 18 травня 2026)", "type": "text", "required": True},
        "landlord_name":   {"label": "ПІБ орендодавця", "type": "text", "required": True},
        "tenant_name":     {"label": "ПІБ орендаря", "type": "text", "required": True},
        "address":         {"label": "Адреса квартири (обл., місто, вул., буд., кв.)", "type": "text", "required": True},
        "area":            {"label": "Площа квартири (кв. м)", "type": "number", "required": True},
        "floor":           {"label": "Поверх", "type": "number", "required": True},
        "transfer_days":   {"label": "Термін передачі (днів)", "type": "number", "required": True},
        "rental_months":   {"label": "Строк оренди (місяців)", "type": "number", "required": True},
        "rent_amount":     {"label": "Розмір орендної плати (грн, цифрами)", "type": "number", "required": True},
        "rent_amount_text":{"label": "Орендна плата (прописом, грн)", "type": "text", "required": True},
        "payment_day":     {"label": "День сплати (число місяця)", "type": "number", "required": True},
        "deposit_amount":  {"label": "Завдаток (грн, цифрами)", "type": "number", "required": False},
        "deposit_amount_text": {"label": "Завдаток (прописом)", "type": "text", "required": False},
        "start_date":      {"label": "Початок дії договору", "type": "text", "required": True},
        "end_date":        {"label": "Кінець дії договору", "type": "text", "required": True},
        "landlord_passport": {"label": "Паспорт орендодавця", "type": "text", "required": True},
        "landlord_id":     {"label": "ІПН орендодавця", "type": "text", "required": True},
        "tenant_passport": {"label": "Паспорт орендаря", "type": "text", "required": True},
        "tenant_id":       {"label": "ІПН орендаря", "type": "text", "required": True},
    }
)

db.add(template)
db.commit()
db.refresh(template)

print(f"[OK] Shablon uspishno dodano! ID = {template.id}")
print(f"   Nazva: {template.name}")
print(f"   Shlyakh: {template.file_path}")
db.close()
