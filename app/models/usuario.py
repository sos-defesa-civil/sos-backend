from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

class Usuario(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255))
    data_nascimento = Column(DateTime)
    cpf = Column(String(14))
    email = Column(String(100))
    senha = Column(String(255))
    admin = Column(Boolean, default=False)

    @declared_attr
    def ocorrencias(cls):
        return relationship("Ocorrencia", back_populates="usuario", foreign_keys="Ocorrencia.user_id")

class Cidadao(Usuario):
    __tablename__ = 'cidadaos'
    endereco = Column(String(255))
    num_ocorrencias_registradas = Column(Integer, default=0)
    telefone = Column(String(15), default=None)
    celular = Column(String(15))

    curtidas = relationship("Curtida", back_populates="usuario")

class Funcionario_Defesa_Civil(Usuario):
    __tablename__ = 'funcionarios_defesa_civil'
    cargo = Column(String(100))
    nivel_acesso = Column(String(100))

    feedbacks = relationship("Feedback", back_populates="usuario")