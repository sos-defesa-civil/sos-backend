from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Midia(Base):
    __tablename__ = 'midias'

    id = Column(Integer, primary_key=True, index=True)
    oc_id = Column(Integer, ForeignKey("ocorrencias.id"))
    tipo = Column(String(100))
    caminho = Column(String(255))

    ocorrencia = relationship("Ocorrencia", back_populates="midias")