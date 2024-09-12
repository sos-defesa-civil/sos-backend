from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OcorrenciaBase(BaseModel):
    user_id: int
    tipo: str
    descricao: str
    data_registro: datetime
    ultima_atualizacao: datetime

class OcorrenciaCreate(OcorrenciaBase):
    pass

class OcorrenciaResponse(OcorrenciaBase):
    id: int

    class Config:
        from_attributes = True
