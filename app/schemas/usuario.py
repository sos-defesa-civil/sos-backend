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
        orm_mode = True

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(UsuarioBase):
    pass

class CidadaoBase(UsuarioBase):
    endereco: str
    num_ocorrencias_registradas: Optional[int]
    telefone: Optional[str]
    celular: str

class CidadaoCreate(UsuarioCreate):
    pass

class CidadaoUpdate(UsuarioUpdate):
    pass

class FuncionarioDefesaCivilBase(UsuarioBase):
    cargo: str
    nivel_acesso: str

class FuncionarioDefesaCivilCreate(UsuarioCreate):
    pass

class FuncionarioDefesaCivilUpdate(UsuarioUpdate):
    pass