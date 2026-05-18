from sqlalchemy import Column, Integer, String, JSON
from database import Base

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    file_path = Column(String)
    fields_config = Column(JSON) # JSON конфігурація для анкети (структура форми)
