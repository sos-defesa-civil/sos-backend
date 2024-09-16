from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class UsuarioBase(BaseModel):
    id: int
    nome: str
    data_nascimento: datetime
    cpf: str
    email: str
    admin: bool

    class Config:
        from_attributes = True

class CidadaoBase(UsuarioBase):
    endereco: str
    num_ocorrencias_registradas: Optional[int]
    telefone: Optional[str]
    celular: str

class CidadaoCreate(CidadaoBase):
    pass

class CidadaoUpdate(CidadaoBase):
    pass

class FuncionarioDefesaCivilBase(UsuarioBase):
    cargo: str
    nivel_acesso: str

class FuncionarioDefesaCivilCreate(FuncionarioDefesaCivilBase):
    pass

class FuncionarioDefesaCivilUpdate(FuncionarioDefesaCivilBase):
    pass