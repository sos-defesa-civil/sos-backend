from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from app.database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    data_nascimento = Column(DateTime)
    cpf = Column(String(14))
    email = Column(String(100))
    senha = Column(String(255))
    admin = Column(Boolean, default=False)