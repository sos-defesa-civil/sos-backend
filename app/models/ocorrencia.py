from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base

class Ocorrencia(Base):
    __tablename__ = 'ocorrencias'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    tipo = Column(String(100))
    descricao = Column(Text)
    data_registro = Column(DateTime)
    ultima_atualizacao = Column(DateTime)