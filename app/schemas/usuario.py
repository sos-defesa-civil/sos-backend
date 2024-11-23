from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    nome: str
    data_nascimento: datetime
    cpf: str
    email: str
    admin: bool

    class Config:
        from_attributes = True  # This allows Pydantic to work with SQLAlchemy models

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioUpdate(UsuarioBase):
    senha: str

class UsuarioResponse(UsuarioBase):
    id: int  # Make sure to include the `id` field if you're returning it in the response

class CidadaoBase(UsuarioBase):
    endereco: str
    num_ocorrencias_registradas: Optional[int]
    telefone: Optional[str]
    celular: str

    class Config:
        from_attributes = True  # Allows interaction with SQLAlchemy objects

class CidadaoResponse(CidadaoBase):
    id: int  # Make sure to include the `id` field in the response

class CidadaoCreate(CidadaoBase):
    senha: str

class CidadaoUpdate(CidadaoBase):
    senha: str

class FuncionarioBase(UsuarioBase):
    cargo: str
    nivel_acesso: str

    class Config:
        from_attributes = True  # Allows interaction with SQLAlchemy objects

class FuncionarioCreate(FuncionarioBase):
    senha: str

class FuncionarioUpdate(FuncionarioBase):
    senha: str

class FuncionarioResponse(FuncionarioBase):
    id: int  # Ensure `id` field is included if it's returned