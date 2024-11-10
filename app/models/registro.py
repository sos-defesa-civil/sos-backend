from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class Registro(Base):
    __tablename__ = "registros"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    data = Column(DateTime, default=datetime.utcnow, nullable=False)
    tipo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
