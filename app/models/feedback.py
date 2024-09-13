from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Feedback(Base):
    __tablename__ = 'feedbacks'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("funcionarios_defesa_civil.id"))
    oc_id = Column(Integer, ForeignKey("ocorrencias.id"))
    titulo = Column(String(100))
    descricao = Column(Text)
    status = Column(String(50))
    data_registro = Column(DateTime)

    ocorrencia = relationship("Ocorrencia", back_populates="feedbacks")
    usuario = relationship("Funcionario_Defesa_Civil", back_populates="feedbacks")
