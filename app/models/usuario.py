from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from app.database import Base
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255))
    data_nascimento = Column(DateTime)
    cpf = Column(String(14), unique=True)
    email = Column(String(100), unique=True)
    senha = Column(String(255))
    admin = Column(Boolean, default=False)

    cidadao = relationship("Cidadao", uselist=False, back_populates="usuario", cascade="all, delete-orphan")
    funcionario = relationship("Funcionario_Defesa_Civil", uselist=False, back_populates="usuario", cascade="all, delete-orphan")
    ocorrencias = relationship("Ocorrencia", back_populates="usuario", foreign_keys="Ocorrencia.user_id", cascade="all, delete-orphan")
    curtidas = relationship("Curtida", back_populates="usuario", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="usuario", cascade="all, delete-orphan")

class Cidadao(Base):
    __tablename__ = 'cidadaos'
    user_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    endereco = Column(String(255))
    num_ocorrencias_registradas = Column(Integer, default=0)
    telefone = Column(String(15), default=None)
    celular = Column(String(15))

    usuario = relationship("Usuario", back_populates="cidadao")

class Funcionario_Defesa_Civil(Base):
    __tablename__ = 'funcionarios_defesa_civil'
    user_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    cargo = Column(String(100))
    nivel_acesso = Column(String(100))

    usuario = relationship("Usuario", back_populates="funcionario")
