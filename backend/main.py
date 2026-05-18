from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

import models
import schemas
from database import engine, get_db
from generator import generate_document

# Створюємо таблиці в базі даних, якщо їх немає
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Онлайн-конструктор договорів API")

# Налаштування CORS для підключення Frontend-частини (Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/templates/", response_model=list[schemas.TemplateResponse])
def get_templates(db: Session = Depends(get_db)):
    """Отримати список доступних шаблонів договорів."""
    templates = db.query(models.Template).all()
    return templates

@app.get("/templates/{template_id}/fields/")
def get_template_fields(template_id: int, db: Session = Depends(get_db)):
    """Отримати JSON-конфігурацію полів (анкети) для конкретного шаблону."""
    template = db.query(models.Template).filter(models.Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Шаблон не знайдено")
    return template.fields_config

@app.post("/generate/{template_id}/")
def generate_and_download(template_id: int, request: schemas.GenerateRequest, db: Session = Depends(get_db)):
    """Згенерувати документ та отримати посилання на нього."""
    template = db.query(models.Template).filter(models.Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Шаблон не знайдено")
    
    if not os.path.exists(template.file_path):
        raise HTTPException(status_code=500, detail="Файл шаблону відсутній на сервері")
        
    result = generate_document(template.file_path, request.data)
    
    # За замовчуванням повертаємо PDF для перегляду у браузері
    if result["pdf_path"] and os.path.exists(result["pdf_path"]):
        return FileResponse(
            result["pdf_path"], 
            media_type="application/pdf", 
            headers={"Content-Disposition": "inline; filename=document.pdf"}
        )
    elif os.path.exists(result["docx_path"]):
        # Якщо PDF не згенерувався (напр. немає LibreOffice), віддаємо DOCX
        return FileResponse(
            result["docx_path"],
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment; filename=document.docx"}
        )
    else:
        raise HTTPException(status_code=500, detail="Помилка при генерації файлу")


