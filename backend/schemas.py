from pydantic import BaseModel
from typing import Dict, Any, List

class TemplateBase(BaseModel):
    name: str
    description: str
    file_path: str
    fields_config: Dict[str, Any]

class TemplateResponse(TemplateBase):
    id: int

    class Config:
        from_attributes = True

class GenerateRequest(BaseModel):
    data: Dict[str, Any] # Дані з форми, відправлені користувачем
