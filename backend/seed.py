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

templates_data = [
    {
        "id": 1,
        "name": "Договір оренди житла",
        "description": "Стандартний договір оренди жилого приміщення між орендодавцем та орендарем",
        "file_name": "dogovir_orendy.docx",
        "fields_config": {
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
    },
    {
        "id": 2,
        "name": "Договір дарування",
        "description": "Договір дарування майна між двома сторонами",
        "file_name": "gift_agreement_template.docx",
        "fields_config": {
            "contract_number": {"label": "Номер договору", "type": "text", "required": True},
            "city": {"label": "Місто укладення", "type": "text", "required": True},
            "date": {"label": "Дата договору", "type": "text", "required": True},
            "donor_name": {"label": "ПІБ дарувальника", "type": "text", "required": True},
            "donee_name": {"label": "ПІБ обдаровуваного", "type": "text", "required": True},
            "gift_description": {"label": "Опис дарунка", "type": "text", "required": True},
            "donor_passport": {"label": "Паспорт дарувальника", "type": "text", "required": True},
            "donor_id": {"label": "ІПН дарувальника", "type": "text", "required": True},
            "donee_passport": {"label": "Паспорт обдаровуваного", "type": "text", "required": True},
            "donee_id": {"label": "ІПН обдаровуваного", "type": "text", "required": True},
        }
    },
    {
        "id": 3,
        "name": "Договір купівлі-продажу",
        "description": "Договір купівлі-продажу транспортного засобу або іншого майна",
        "file_name": "purchase_agreement_template.docx",
        "fields_config": {
            "contract_number": {"label": "Номер договору", "type": "text", "required": True},
            "city": {"label": "Місто укладення", "type": "text", "required": True},
            "date": {"label": "Дата договору", "type": "text", "required": True},
            "seller_name": {"label": "ПІБ продавця", "type": "text", "required": True},
            "buyer_name": {"label": "ПІБ покупця", "type": "text", "required": True},
            "item_description": {"label": "Опис товару (майна)", "type": "text", "required": True},
            "price": {"label": "Ціна (грн, цифрами)", "type": "number", "required": True},
            "price_text": {"label": "Ціна (прописом)", "type": "text", "required": True},
            "seller_passport": {"label": "Паспорт продавця", "type": "text", "required": True},
            "seller_id": {"label": "ІПН продавця", "type": "text", "required": True},
            "buyer_passport": {"label": "Паспорт покупця", "type": "text", "required": True},
            "buyer_id": {"label": "ІПН покупця", "type": "text", "required": True},
        }
    }
]

for t_data in templates_data:
    existing = db.query(models.Template).filter(models.Template.id == t_data["id"]).first()
    if existing:
        print(f"Шаблон '{t_data['name']}' вже існує.")
        continue

    template_path = os.path.join(os.path.dirname(__file__), "..", "templates", t_data["file_name"])
    template_path = os.path.normpath(template_path)

    if not os.path.exists(template_path):
        print(f"ПОМИЛКА: Файл {t_data['file_name']} не знайдено за шляхом {template_path}")
        continue

    template = models.Template(
        name=t_data["name"],
        description=t_data["description"],
        file_path=template_path,
        fields_config=t_data["fields_config"]
    )
    db.add(template)
    db.commit()
    db.refresh(template)
    print(f"[OK] Шаблон '{template.name}' успішно додано!")

db.close()
