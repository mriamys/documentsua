import os
import uuid
import subprocess
from docxtpl import DocxTemplate

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

def generate_document(template_path: str, context: dict) -> dict:
    """
    Підставляє дані в DOCX шаблон та конвертує в PDF.
    """
    # 1. Завантажуємо шаблон
    doc = DocxTemplate(template_path)
    
    # 2. Рендеримо з даними від користувача
    doc.render(context)
    
    # 3. Зберігаємо новий DOCX у тимчасову папку
    unique_id = str(uuid.uuid4())
    docx_filename = f"{unique_id}.docx"
    docx_path = os.path.join(TEMP_DIR, docx_filename)
    doc.save(docx_path)
    
    # 4. Конвертуємо у PDF за допомогою LibreOffice Headless
    # Це вимагає наявності встановленого LibreOffice на сервері.
    pdf_path = os.path.join(TEMP_DIR, f"{unique_id}.pdf")
    try:
        subprocess.run([
            "soffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            TEMP_DIR,
            docx_path
        ], check=True)
    except Exception as e:
        print(f"Помилка конвертації LibreOffice: {e}")
        # Якщо LibreOffice немає, повертаємо тільки DOCX
        return {"docx_path": docx_path, "pdf_path": None}

    return {"docx_path": docx_path, "pdf_path": pdf_path}
