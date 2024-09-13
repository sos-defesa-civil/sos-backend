from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Ocorrencia(Base):
    __tablename__ = 'ocorrencias'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"))
    tipo = Column(String(100))
    descricao = Column(Text)
    data_registro = Column(DateTime)
    ultima_atualizacao = Column(DateTime)

    usuario = relationship("Usuario", back_populates="ocorrencias")
    feedbacks = relationship("Feedback", back_populates="ocorrencia")
    curtidas = relationship("Curtida", back_populates="ocorrencia")
    midias = relationship("Midia", back_populates="ocorrencia")