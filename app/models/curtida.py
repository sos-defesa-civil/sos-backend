from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Curtida(Base):
    __tablename__ = 'curtidas'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("cidadaos.id"))
    oc_id = Column(Integer, ForeignKey("ocorrencias.id"))
    data_registro = Column(DateTime)

    usuario = relationship("Cidadao", back_populates="curtidas")
    ocorrencia = relationship("Ocorrencia", back_populates="curtidas")
