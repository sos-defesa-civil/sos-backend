from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255))
    data_nascimento = Column(DateTime)
    cpf = Column(String(14))
    email = Column(String(100))
    senha = Column(String(255))
    admin = Column(Boolean, default=False)

    cidadao = relationship("Cidadao", uselist=False, back_populates="usuario")
    funcionario = relationship("Funcionario_Defesa_Civil", uselist=False, back_populates="usuario")

    @declared_attr
    def ocorrencias(cls):
        return relationship("Ocorrencia", back_populates="usuario", foreign_keys="Ocorrencia.user_id")

class Cidadao(Base):
    __tablename__ = 'cidadaos'
    user_id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    endereco = Column(String(255))
    num_ocorrencias_registradas = Column(Integer, default=0)
    telefone = Column(String(15), default=None)
    celular = Column(String(15))

    usuario = relationship("Usuario", back_populates="cidadao")
    curtidas = relationship("Curtida", back_populates="usuario")

class Funcionario_Defesa_Civil(Base):
    __tablename__ = 'funcionarios_defesa_civil'
    user_id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    cargo = Column(String(100))
    nivel_acesso = Column(String(100))

    usuario = relationship("Usuario", back_populates="funcionario")
    feedbacks = relationship("Feedback", back_populates="usuario")